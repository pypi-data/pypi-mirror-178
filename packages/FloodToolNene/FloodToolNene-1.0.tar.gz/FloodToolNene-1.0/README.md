# Flood Risk Prediction tool

### Installation Guide

By using the command: 
```
pip install FloodToolNene
```

### User instructions

### 📖Tool Class
After installation, to add the module by running:
```
from flood_tool import *
```

To begin with, you can creat an object named tool:
```
tool = Tool(postcode_file='', sample_labels='', household_file='')
```
The postcode_file, sample_labels and household_file are Filename of a .csv file containing geographic location data for postcodes, the train data and information on households by postcode respectively. **The defalut files will be used if there is no input.**

Next, train your tool with the function `train()` or use `load()` directly:
```
tool.train(labelled_samples='')
tool.load()
```
The labelled_samples is the Filename of a .csv file containing a labelled set of samples which is used to train all the models for prediction( *But in our function, this input is useless, because we preprocess the labelled data inputted in __init__*). **The defalut files will be used if there is no input.** Additionally, when you use the train function, your trained models will be saved in the folder *weights*, and you can use it directly by using load function without re-training your model in the same data.

Now, you can use all the functions inside now! 🎉🎉🎉

**Functions Usage**
```
Tool.get_useful_features(postcodes, features=['sector', 'easting', 'northing', 'localAuthority', 'altitude', 'soilType'])
```
From this function, you can input your sequence of postcodes in `postcodes`, and the features' name you need in `features`. Then, the function will return a dataframe of all features you need index with postcodes. **⚠️The postcodes should be all contained in postcode_file.⚠️**

```
Tool.get_easting_northing(postcodes)
```
From this function, you can get a dataframe with the postcode as the index containing the eastings and northings. **⚠️The postcodes should be all contained in postcode_file.⚠️**

```
Tool.get_lat_long(postcodes)
```
From this function, you can get a dataframe with the postcode as the index containing the GPS latitude and longitude. **⚠️The postcodes should be all contained in postcode_file.⚠️**

```
get_flood_class_from_postcodes_methods()
```
From this function, it will return all possible model can be used to predict the flood class from postcodes. **🥳This function can be used independently.🥳**

```
Tool.get_flood_class_from_postcodes(postcodes, method=1)
```
From this function, you can predict the flood class by a collection of poscodes. It will return a Series of flood risk classification labels indexed by postcodes. **You can choose different methods/models to predict by changing the value of method.** 
 - When `method=0` or `method=get_flood_class_from_postcodes_methods()['all_zero_risk']`, the function will result all the postcodes in the lowest risk.
 - **(Default)** When `method=1` or `method=get_flood_class_from_postcodes_methods()['RandomForestClassifier']`, the *RandomForestClassifier* will be used to predict the flood class.
 
```
get_flood_class_from_locations_methods()
```
From this function, it will return all possible model can be used to predict the flood class from OSGB36 locations or WGS84 locations. **🥳This function can be used independently.🥳**

```
Tool.get_flood_class_from_OSGB36_locations(eastings, northings, method=1)
```
From this function, you can predict the flood class by a collection of OSGB36_locations. It will return a Series of flood risk classification labels indexed by postcodes. **You can choose different methods/models to predict by changing the value of method.** 
 - When `method=0` or `method=get_flood_class_from_locations_methods()['Do Nothing']`, the function will result all the locations in the lowest risk.
 - **(Default)** When `method=1` or `method=get_flood_class_from_locations_methods()['RandomForestClassifier']`, the *RandomForestClassifier* will be used to predict the flood class.
 
```
Tool.get_flood_class_from_WGS84_locations(latitudes, longitudes, rad=False, method=0)
```
From this function, you can predict the flood class by a collection of OSGB36_locations. It will return a Series of flood risk classification labels indexed by postcodes. **You can choose different methods/models to predict by changing the value of method.** 
 - rad: If True, input latitudes and longitudes are in radians.
 - When `method=0` or `method=get_flood_class_from_locations_methods()['Do Nothing']`, the function will result all the locations in the lowest risk.
 - **(Default)** When `method=1` or `method=get_flood_class_from_locations_methods()['RandomForestClassifier']`, the *RandomForestClassifier* will be used to predict the flood class.
 
```
get_house_price_methods()
```
From this function, it will return all possible models can be used to predict the house price from postcodes. **🥳This function can be used independently.🥳**

```
Tool.get_median_house_price_estimate(postcodes, method=2)
```
From this function, you can predict the flood class by a collection of OSGB36_locations. It will return a Series of median house price estimates indexed by postcodes. **You can choose different methods/models to predict by changing the value of method.** **⚠️The postcodes should be all contained in postcode_file.⚠️**
 - When `method=0` or `method=get_house_price_methods()['all_england_median']`, the function will return the all england median in every postcodes.
 - When `method=1` or `method=get_house_price_methods()['KNeighborsRegressor_total_value']`, the *KNeighborsRegressor* fitted with all price data will be used to predict the median house price.
 - **(Default)** When `method=2` or `method=get_house_price_methods()['KNeighborsRegressor_split_price_area']`, the *KNeighborsRegressor* fitted with lower price(lower than £1000000) data will be used to predict the median house price.

```
get_local_authority_methods()
```
From this function, it will return all possible models can be used to predict the local authority from OSGB36 locations. **🥳This function can be used independently.🥳**

```
Tool.get_local_authority_estimate(eastings, northings, method=1)
```
From this function, you can predict the flood class by a collection of OSGB36_locations. It will return a Series of flood risk classification labels indexed by postcodes. **You can choose different methods/models to predict by changing the value of method.** 
 - When `method=0` or `method=get_local_authority_methods()['Do Nothing']`, the function will result all the locations in the Unknown.
 - **(Default)** When `method=1` or `method=get_local_authority_methods()['RandomForestClassifier']`, the *RandomForestClassifier* will be used to predict the local authority.
 
```
Tool.get_total_value(postal_data)
```
From this function, you can input a *Sequence of postcode units or postcodesectors*, and a series of estimates of the total property values of the sequence of postcode units or postcode sectors will be returned.

```
Tool.get_annual_flood_risk(postcodes, risk_labels=None)
```
From this function, you can input a *Sequence of postcodes* and the *setted risk labels* of the postcodes, and Series of total annual flood risk estimates indexed by locations will be returned.
 - If the `risk_label=None`, the function will predict the risk labels and median house price of these postcodes by using default model in `get_flood_class_from_postcodes(postcodes, method=1)` and `get_median_house_price_estimate(postcodes, method=2)`.

# Live.py

📖get_station_data_from_csv Function

This function returns the value reading for a specified recording station. This value may be a tidal level in mAOD, rainfall measurements in mm or stage level in mASD from a csv when the csv fiilename and a station reference are passed. See example below.

```
get_station_data_from_csv(filename, station_reference)
```


📖get_live_station_data Function

This function returns a DataFrame showing showing the coordinates in lat/long as wells as the parameter type (i.e. level or rainfall) and the latest reading in realtime when a station reference is passed.  All station referneces that cannot be found online return for example 'stationn reference '233f' ccannot be found live'. If a station reference exists online, but some features are not available, these features are denoted as 'Unavailable'. See an example below.

```
get_live_station_data(station_reference)
```
### Geo.py

In the file Geo.py methods for geographical conversions can be found. 


The class **Epsiloid** contains:

**dms2rad**, which converts degrees, minutes, and seconds to radians, returning a numpy array.

**rad2dms**, which converts radians to degrees, minutes, and seconds, returning a numpy array.

**lat_long_to_xyz**, which converts latitude and longitude coordinates to Cartesian (x,y,z) coordinates.

**xyz_to_lat_long**, which converts Cartesian coordinates to latitude and longitude.

**get_easting_northing_from_gps_lat_long**, which takes latitude and longitude coordinates to easting and northing GPS locations.

**bigM**, which takes the ellipsoid semi major axis, central meridian scale, n, and a latitude or longitude to compute the meridional arc.

**get_gps_lat_long_from_easting_northing**, which takes easting and northing GPS locations and converts them to latitude and longitude coordinates.



The class **HelmertTransform** contains:

**WGS84toOSGB36**. which takes WGS84 latitude/longitude coordinates and converts them to OSGB36 latitude/longitude coordinates.

**OSGB36toWGS84**, which takes OSGB36 latitude/longitude coordinates and converts them to WGS84 latitude/longitude coordinates.

To use these functions, you can use:
```
from .geo import *
```


### Visualizations
 After installation, you can download the visualization preprocessing and plotting functions by running:
 ```
from flood_tools import visual_methods
```
To begin with, you can first create the object of the visual class **Preprocess** and class **Visualize** to preprocess the data for plotting different kind of plots.

```
preprocess = visual_methods.Preprocess(price="", risk_label="", station_data = "" , annual_risk = "")
map = visual_methods.Visualize(price = "", risk_label = "", annual_risk = "")
```
_The classes take file paths as its parameters and have been initialized with sample files in the repository_
price="flood_tool/resources/predicted_data.csv",
risk_label="flood_tool/resources/prediction_riskLabel.csv"
station_data="flood_tool/resources/stations.csv"
annual_risk = "flood_tool/resources/AnnualRiskPredict.csv"

**price** takes the predicted median house price dataset in .csv format which includes the easting, northing and predicted values.
**risk_label** takes the easting, northing and the predicted risk_label dataset in .csv format.
**annual_risk** takes the easting, northing and the predicted total annual risk (combining the risk label and total values of households) dataset in .csv format.
**station_data** is the provided station data .csv file to compare the latitude and longitude values for different station references from the typical and wet day dataset.

All the initialized files are saved in the flood_tool/resources in similar names.

Now, you can use all the functions inside now! 🎉🎉🎉
```
Preprocess.merge(filename)
```
This function takes input of filename and merges it with the station data to compare and get the location (latitude/longitude) for the given station refrence numbers.

```
Preprocess.get_class(filename)
```
This function takes input of filename and splits the continous values of rainfall and river/tidal leve data into different classes (eg: high/medium/low) based on defined metrics.

```
Preprocess.house_price_preprocess()
```
This function is used to preprocess the house_price data. It creates the latitude and longitude columns by using the geo.py module to convert the easting northing to latitude longitude. It also ceates a "class" column to split the dataset based on the quartile it falls in, i.e. 

| House price | classifier |
|:--------:|:----------:|
| <25% | 0 |
| between 25% and 50%| 1 |
| between 50% and 75%| 2 |
| >75% | 3 |

The function returns the preprocessed dataframe with the classes, latitude, longitude and Median_price columns.

```
Preprocess.risk_label_preprocess()
```
This function is used to preprocess the risk_label data. It creates the latitude and longitude columns by using the geo.py module to convert the easting northing to latitude longitude and returns the new dataframe. 

```
Preprocess.Annual_risk_preprocess()
```
This function is used to preprocess the annual_risk data. It creates the latitude and longitude columns by using the geo.py module to convert the easting northing to latitude longitude and returns the new dataframe.
 
 ```
Preprocess.zip_data(dataframe)
```
This function creates a list of the list of the latitude, longitude and value for plotting in folium.

### Visualize class

```
Visualize.plot_HeatMapWithTime(dataframe)
```
This function plots a heat map with time for timeseries datasets provided, the rainfall and tidal level datasets for a wet and typical day.

```
Visualize.plot_class_map(dataframe_wet_day, dataframe_typical_day,key="rainfall")
```
This function plots Class distribution for Rainfall and Tidal/River Level (Typical/Wet day)
parameter "key" will have two values: rainfall or river
        # --class: is for both raninfall and river with the classification
        # --value: is for both rainfall and river with the original value
        # --percentage: only for river which has the high and low record
        
This function can deal with rain and river data seperately.

```
Visualize.house_price_map()
```
This function can plot the predicted median house prices on a folium map. It shows the class distribution of the prices

```
Visualize.risk_label_map()
```
This function can plot the predicted flood risk labels (from 1-10) on a folium map

```
Visualize.AnnualRisk_map()
```
This function can plot the predicted annual flood risk on a folium map based on a custom classification

| Annual risk on log scale| classifier |
|:--------:|:----------:|
| <2.2 | 0 |
| between 2.2 and 6| 1 |
|>6| 2 |
This classification is done by looking at the histogram distribution of the predicted risks.

### Documentation

_This section should be updated during the week._

The code includes [Sphinx](https://www.sphinx-doc.org) documentation. On systems with Sphinx installed, this can be build by running

```
python -m sphinx docs html
```

then viewing the generated `index.html` file in the `html` directory in your browser.

For systems with [LaTeX](https://www.latex-project.org/get/) installed, a manual pdf can be generated by running

```bash
python -m sphinx  -b latex docs latex
```

Then following the instructions to process the `FloodTool.tex` file in the `latex` directory in your browser.

### Testing

The tool includes several tests, which you can use to check its operation on your system. With [pytest](https://doc.pytest.org/en/latest) installed, these can be run with

```bash
python -m pytest --doctest-modules flood_tool
```

Additionally, we write a test to check our tool.py. You can use it first cd the folder *tests*, and run the **test_tool.py**.

### Reading list

 - (A guide to coordinate systems in Great Britain)[https://webarchive.nationalarchives.gov.uk/20081023180830/http://www.ordnancesurvey.co.uk/oswebsite/gps/information/coordinatesystemsinfo/guidecontents/index.html]

 - (Information on postcode validity)[https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/283357/ILRSpecification2013_14Appendix_C_Dec2012_v1.pdf]
