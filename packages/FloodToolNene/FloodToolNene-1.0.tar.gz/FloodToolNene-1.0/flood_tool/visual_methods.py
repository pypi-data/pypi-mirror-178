import pandas as pd
from folium.plugins import HeatMap, HeatMapWithTime
import folium
from .geo import *
import numpy as np
import branca.colormap as cm
from branca.element import Template, MacroElement

colors_price = [
    'green',
    'blue',
    'red',
    'yellow'
]
colors_flood = ['lightgreen','green','darkgreen','beige', 'blue','orange','pink',
        'lightred', 'red','darkred',"purple"]

def colorCall_price(val):
  val = int(val)
  return colors_price[val]

def colorCall_flood(val):
  val = int(val)
  return colors_flood[val]

def func_rainfall_class(x):
    if x < 2:
        return 0
    elif x < 4:
        return 1
    elif x < 50:
        return 2
    return 3


class Preprocess:
    def __init__(self,price="flood_tool/resources/predicted_data.csv",
    risk_label="flood_tool/resources/prediction_riskLabel.csv",
    station_data="flood_tool/resources/stations.csv",
    annual_risk = "flood_tool/resources/AnnualRiskPredict.csv"):

        self.house_price = pd.read_csv(price)
        self.risk_label = pd.read_csv(risk_label)
        self.station_data = pd.read_csv(station_data)
        self.annual_risk = pd.read_csv(annual_risk)

    def merge(self, filename):
        
        """Merge the given data with a station to get location information.
        
        Parameters
        ----------

        filename: path to datafram to be read in via read_csv."""
        
        data = pd.read_csv(filename)
        data = pd.merge(data, self.station_data, how="left", on="stationReference")
        data = data.dropna(subset=["latitude", "longitude"])
        data["value"] = data["value"].apply(lambda x: x if isinstance(x, str) else str(x))
        index = data["value"].apply(lambda x: False if '|' in x else True)
        data = data[index]
        data["value"] = data["value"].apply(lambda x: float(x))

        rainfall = data[data["parameter"] == "rainfall"]
        river = data[data["parameter"] == "level"]
        return rainfall, river

    def get_class(self,filename):
        
        """Calculate the class (high or low) for rainfall and river data using 
        percentages and typical high and low range data for each station.
        
        Parameters
        ----------

        filename: path to datafram to be read in via read_csv."""
        
        rainfall,river = self.merge(filename)
        rainfall = rainfall.groupby("stationReference")["value"].mean() * 4
        rainfall_df = rainfall.to_frame()
        rainfall_df = rainfall_df.reset_index()
        rainfall_df["class"] = rainfall_df["value"].apply(lambda x: func_rainfall_class(x))
        rainfall_df = pd.merge(rainfall_df, self.station_data, how="left", on="stationReference")

        river_result = river.groupby("stationReference")["value"].mean()
        river_result_df = river_result.to_frame()
        river_result_df = river_result_df.reset_index()
        river_result_df = pd.merge(river_result_df, self.station_data, how="left", on="stationReference")
        vs = river_result_df["value"].tolist()
        highs = river_result_df["typicalRangeHigh"].tolist()
        lows = river_result_df["typicalRangeLow"].tolist()
        class_list = []
        percentage_list = []
        for v, h, l in zip(vs, highs, lows):
            if v > h:
                class_list.append(2)
            elif v < l:
                class_list.append(0)
            else:
                class_list.append(1)
            percentage_list.append((v - l) / (h - l))
        river_result_df["class"] = class_list
        river_result_df["percentage"] = percentage_list
        return rainfall_df, river_result_df
   

    def house_price_preprocess(self):
        
        """Preprocess the house price data to get it ready for visualization 
        through defining high, medium, and low prices."""
        
        coord = []
        for i in range(len(self.house_price)):
            coord.append(get_gps_lat_long_from_easting_northing(self.house_price["easting"][i],
                                                                self.house_price["northing"][i]))
        self.house_price["lat"] = [x[0][0] for x in coord]
        self.house_price["long"] = [x[1][0] for x in coord]
        price = self.house_price[['lat', 'long', 'predicted_MedianPrice']]

        def func(x):
            if x < np.percentile(price["predicted_MedianPrice"],25):
                return 0
            elif x < np.percentile(price["predicted_MedianPrice"],50):
                return 1
            elif np.percentile(price["predicted_MedianPrice"],75):
                return 2
            return 3

        price["class"] = price["predicted_MedianPrice"].apply(lambda x: func(x))
        return price
    
    def risk_label_preprocess(self):
        
        """Preprocess the risk label data by converting easting/northing to latitude/longitude."""
        
        coord = []
        for i in range(len(self.risk_label)):
            coord.append(get_gps_lat_long_from_easting_northing(self.risk_label["easting"][i],
                                                                self.risk_label["northing"][i]))
        self.risk_label["lat"] = [x[0][0] for x in coord]
        self.risk_label["long"] = [x[1][0] for x in coord]
        risk_predictions = self.risk_label[['lat', 'long', 'riskLabel']]

        return risk_predictions
    
    def Annual_risk_preprocess(self):
        coord = []
        for i in range(len(self.annual_risk)):
            coord.append(get_gps_lat_long_from_easting_northing(self.annual_risk["easting"][i],
                                                                self.annual_risk["northing"][i]))


        self.annual_risk["lat"] = [x[0][0] for x in coord]
        self.annual_risk["long"] = [x[1][0] for x in coord]
        risk_predictions = self.annual_risk[['lat', 'long', 'AnnualRisk']]
        risk_predictions["AnnualRisk"] = np.log(risk_predictions["AnnualRisk"])

        def func(x):
            if x < 2.2:
                return 0
            elif x < 6:
                return 1
            else:return 2

        risk_predictions["class"] = risk_predictions["AnnualRisk"].apply(lambda x: func(x))
        return risk_predictions


    def zip_data(self, data_df, key="value"):
        
        """Zip the latitude/longitude and value, which has the key name of parameter key.
        
        Parameters
        ----------

        data_df: path to file to read in through pd.read_csv."""
        
        lat = data_df["latitude"].tolist()
        lon = data_df["longitude"].tolist()
        v = data_df[key].tolist()
        return list(zip(lat, lon, v))


class Visualize():

    def __init__(self,price="flood_tool/resources/predicted_data.csv",
    risk_label="flood_tool/resources/prediction_riskLabel.csv",
    annual_risk = "flood_tool/resources/AnnualRiskPredict.csv"):
        self.house_price = pd.read_csv(price)
        self.risk_label = pd.read_csv(risk_label)
        self.annual_risk = pd.read_csv(annual_risk)


    def plot_HeatMapWithTime(self, data):
        # using datetime to plot the original value of the inputed data
        date_time = list(data["dateTime"].sort_values().astype("str").unique())
        loc = 'Heat map of Rainfall/Level distribution with time over a wet/typical day'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)
        tdata = []
        for _, d in data.groupby("dateTime"):
            tdata.append([[row["latitude"], row["longitude"], row["value"]] for _, row in d.iterrows()])
        map = folium.Map([51.4, 0.3], zoom_start=7, control_scale=True)
        map.get_root().html.add_child(folium.Element(title_html))
        HeatMapWithTime(tdata, index=date_time, radius=30).add_to(map)
        return map   

    def plot_wet_and_typical_class(self, wet_data_c, ty_data_c, key="value"):
        
        """Create plot of river and rainfall data on wet and typical days.
        
        Parameters
        ----------

        wet_data_c: path to data on a wet day in the United Kingdom, in terms of river level
        ty_data_c: path to data on a typical day in the United Kingdom, in terms of river level"""

        loc = 'Comparing Wet Day and Typical Day distributions'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)
        
        if key == "percentage":
            wet_data_c = wet_data_c.dropna(subset=["percentage"])
            ty_data_c = ty_data_c.dropna(subset=["percentage"])
        
        wet_river_zip = Preprocess.zip_data(self,wet_data_c, key)
        ty_river_zip = Preprocess.zip_data(self,ty_data_c, key)
        map = folium.Map([52.5, 0.], zoom_start=6,zoom_end=15,control_scale=True)
        map.get_root().html.add_child(folium.Element(title_html))
        layer_wet_river = folium.FeatureGroup(name="Wet day")
        layer_typical_river = folium.FeatureGroup(name="Typical day")
        HeatMap(wet_river_zip, radius=15).add_to(layer_wet_river)
        HeatMap(ty_river_zip, radius=15).add_to(layer_typical_river)
        map.add_child(layer_wet_river)
        map.add_child(layer_typical_river)
        map.add_child(folium.map.LayerControl())
        return map

    def plot_heat_map(self, data):
        
        """Create heatmap using datetime to plot the original value of the data.
        
        Parameters
        ----------

        data: path to dataframe."""
        
        date_time = list(data["dateTime"].sort_values().astype("str").unique())
        tdata = []
        for _, d in data.groupby("dateTime"):
            tdata.append([[row["latitude"], row["longitude"], row["value"]] for _, row in d.iterrows()])
        map = folium.Map([53, 0.3], zoom_start=8, control_scale=True)
        HeatMapWithTime(tdata, index=date_time, radius=20).add_to(map)
        return map

    def plot_class_map(self, wet_data_c, ty_data_c, type="rainfall"):
        
        """Create a visualization of the class (defined in get_class) of rainfall on a wet and typical day.
        
        Parameters
        ----------

        wet_data_c: path to data on a wet day in the United Kingdom, in terms of rainfall
        ty_data_c: path to data on a typical day in the United Kingdom, in terms of rainfall"""
        
        wet_zip = Preprocess.zip_data(self,wet_data_c, "class")
        ty_zip = Preprocess.zip_data(self,ty_data_c, "class")

        loc = 'Class distribution for Rainfall and Tidal/River Level (Typical/Wet day)'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)

        map = folium.Map([51.4,0.], zoom_start=7, control_scale=True)
        map.get_root().html.add_child(folium.Element(title_html))
        

        layer_wet = folium.FeatureGroup(name="Wet day")
        layer_typical = folium.FeatureGroup(name="Typical day")
        if type == "rainfall":
            layer_wet = self.plot_rain_class(wet_zip, layer_wet)
            layer_typical = self.plot_rain_class(ty_zip, layer_typical)
        else:
            layer_wet = self.plot_river_class(wet_zip, layer_wet)
            layer_typical = self.plot_river_class(ty_zip, layer_typical)
        map.add_child(layer_wet)
        map.add_child(layer_typical)
        map.add_child(folium.map.LayerControl())
        return map
    
    def plot_rain_class(self, data, map):

        """Create a visualization of the rainfall classes.
        Classes are 
        slight: <2mm per hour,
        moderate: 2-4mm per hour,
        high: 4-50mm per hour,
        violent: >50mm per hour"""
        
        radiuses = [2000, 5000, 8000, 10000]

        colormap = ["green", "yellow", "red", "black"]
        
        template = """
        {% macro html(this, kwargs) %}
        
        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
            
        <div class='legend-title'>Risk Label Legend</div>
        <ul class='legend-labels'>
            <li><span style='background:green;opacity:0.7;'></span>slight rainfall(<2mm per hr)</li>
            <li><span style='background:blue;opacity:0.7;'></span>moderate rainfall(2mm-4mm per hr)</li>
            <li><span style='background:red;opacity:0.7;'></span> high rainfall(4mm-50mm per hr)</li>
            <li><span style='background:yellow;opacity:0.7;'></span>violent rainfall(>50mm per hr)</li>
            
        </ul>
        </div>
        
        </body>
        </html>

        <style type='text/css'>
        .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
        .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
        .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
        .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
        .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
        .maplegend a {
            color: #777;
            }
        </style>
        {% endmacro %}"""

        macro = MacroElement()
        macro._template = Template(template)


        map.get_root().add_child(macro)
        for la, lo, c in data:
            folium.Circle(location=(la, lo), radius=radiuses[c], color=colormap[c], popup=c, fill=True,
                          fill_opacity=0.7).add_to(map)
        
        
        return map

    def plot_river_class(self, data, map):

        
        """Create a visualization for the river classes which are 
        low: lower than typical river level, 
        normal: between low and high,
        high: greater than typical river level"""

        radiuses = [3000, 2000, 10000]

        colormap = ["green", "yellow", "red"]
        template = """
        {% macro html(this, kwargs) %}
        
        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
            
        <div class='legend-title'>Risk Label Legend</div>
        <ul class='legend-labels'>
            <li><span style='background:green;opacity:0.7;'></span>Level lower than typical low</li>
            <li><span style='background:yellow;opacity:0.7;'></span>Normal (between typical high and low)</li>
            <li><span style='background:red;opacity:0.7;'></span> Level higher than typical high</li>
            
            
        </ul>
        </div>
        
        </body>
        </html>

        <style type='text/css'>
        .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
        .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
        .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
        .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
        .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
        .maplegend a {
            color: #777;
            }
        </style>
        {% endmacro %}"""

        macro = MacroElement()
        macro._template = Template(template)
        map.get_root().add_child(macro)
        

        for la, lo, c in data:
            folium.Circle(location=(la, lo), radius=radiuses[c], color=colormap[c], popup=c, fill=True,
                          fill_opacity=0.7).add_to(map)
        
        return map

    def house_price_map(self):
        
        """Create a circle plot to visualize the median house price in different postcodes of the United Kingdom"""
        
        price = Preprocess.house_price_preprocess(self)
        import branca.colormap as cm
        cs = price["class"]

        data = zip(price["lat"],price["long"],cs)

        loc = 'Predicted Median House Prices'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)

        map = folium.Map([51.4,0.], zoom_start=8,zoom_end =15)

        map.get_root().html.add_child(folium.Element(title_html))

        for la,lo,c in data:
            folium.Circle(location=(la,lo),radius=1000,popup=c,color=False,
            fill_color = colorCall_price(c),fill=True,fill_opacity=0.5).add_to(map)

        template = """
        {% macro html(this, kwargs) %}
        
        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
            
        <div class='legend-title'>Risk Label Legend</div>
        <ul class='legend-labels'>
            <li><span style='background:green;opacity:0.7;'></span>Very Low prices (0-25%)</li>
            <li><span style='background:blue;opacity:0.7;'></span>Low prices (25%-50%)</li>
            <li><span style='background:red;opacity:0.7;'></span>High prices (50%-75%)</li>
            <li><span style='background:yellow;opacity:0.7;'></span>Ver High prices(above 75%)</li>
            
        </ul>
        </div>
        
        </body>
        </html>

        <style type='text/css'>
        .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
        .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
        .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
        .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
        .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
        .maplegend a {
            color: #777;
            }
        </style>
        {% endmacro %}"""

        macro = MacroElement()
        macro._template = Template(template)

        map.get_root().add_child(macro)
        return map


    def risk_label_map(self):
        
        """Create a circle plot to visualize the risk label for different postcodes in the United Kingdom.
        Risk label describes how at risk a property is of flooding."""

        risk_predictions = Preprocess.risk_label_preprocess(self)
        cs = risk_predictions["riskLabel"]

        data = zip(risk_predictions["lat"],risk_predictions["long"],cs)

        

        loc = 'Predicted Flood risk'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)

        map = folium.Map([51.3,0.], zoom_start=8,zoom_end =15)

        map.get_root().html.add_child(folium.Element(title_html))


        for la,lo,c in data:
            radius = ((c+1)*10)**2
            folium.Circle(location=(la,lo),radius=radius,color=False,
            fill_color = colorCall_flood(c),fill=True,fill_opacity=0.5).add_to(map)

        
        template = """
        {% macro html(this, kwargs) %}
        
        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
            
        <div class='legend-title'>Risk Label Legend</div>
        <ul class='legend-labels'>
            <li><span style='background:green;opacity:0.3;'></span>1</li>
            <li><span style='background:green;opacity:0.5;'></span>2</li>
            <li><span style='background:green;opacity:0.8;'></span>3</li>
            <li><span style='background:yellow;opacity:0.3;'></span>4</li>
            <li><span style='background:blue;opacity:0.3;'></span>5</li>
            <li><span style='background:blue;opacity:0.5;'></span>6</li>
            <li><span style='background:orange;opacity:0.5;'></span>7</li>
            <li><span style='background:red;opacity:0.3;'></span>8</li>
            <li><span style='background:red;opacity:0.5;'></span>9</li>
            <li><span style='background:red;opacity:0.7;'></span>10</li>

        </ul>
        </div>
        
        </body>
        </html>

        <style type='text/css'>
        .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
        .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
        .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
        .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
        .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
        .maplegend a {
            color: #777;
            }
        </style>
        {% endmacro %}"""

        macro = MacroElement()
        macro._template = Template(template)

        map.get_root().add_child(macro)


        return map


    def AnnualRisk_map(self):
        
        """Create a visualization of predicted annual flood risk to properties
        on a scale of low, medium, high."""
        
        loc = 'Predicted Annual Flood risk to property'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)

        AnnualRisk = Preprocess.Annual_risk_preprocess(self)
        import branca.colormap as cm
        cs = AnnualRisk["class"]

        data = zip(AnnualRisk["lat"],AnnualRisk["long"],cs)

        loc = 'Predicted Annual Flood risk to property'
        title_html = '''
                    <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                    '''.format(loc)

        map = folium.Map([51.4,0.], zoom_start=8,zoom_end =15)

        map.get_root().html.add_child(folium.Element(title_html))

        for la,lo,c in data:
            radius = (c+1)*500
            folium.Circle(location=(la,lo),radius=radius,popup=c,color=False,
            fill_color = colorCall_price(c),fill=True,fill_opacity=0.5).add_to(map)

        template = """
        {% macro html(this, kwargs) %}
        
        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
            
        <div class='legend-title'>Risk Label Legend</div>
        <ul class='legend-labels'>
            <li><span style='background:green;opacity:0.7;'></span> Low flood risk</li>
            <li><span style='background:blue;opacity:0.7;'></span>Medium flood risk</li>
            <li><span style='background:red;opacity:0.7;'></span>High flood risk</li>
            
        </ul>
        </div>
        
        </body>
        </html>

        <style type='text/css'>
        .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
        .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
        .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
        .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
        .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
        .maplegend a {
            color: #777;
            }
        </style>
        {% endmacro %}"""

        macro = MacroElement()
        macro._template = Template(template)

        map.get_root().add_child(macro)
        return map

