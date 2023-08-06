"""Interactions with rainfall and river data."""

import numpy as np
import pandas as pd

__all__ = ["get_station_data_from_csv"]


def get_station_data_from_csv(filename, station_reference):
    """Return readings for a specified recording station from .csv file.

    Parameters
    ----------

    filename: str
        filename to read
    station_reference
        station_reference to return.

    >>> data = get_station_data_from_csv('resources/wet_day.csv')
    """
    frame = pd.read_csv(filename)
    frame = frame.loc[frame.stationReference == station_reference]

    return pd.to_numeric(frame.value.values)

def get_live_station_data(station_reference):
    
    """Return readings for a specified recording station from live API as a DataFrame.

    Parameters
    ----------

    station_reference: str or list/ndarray of str 
        station_reference to return.

    >>> data = get_live_station_data('0184TH')
    """
    
    assert isinstance(station_reference, str) or isinstance(station_reference, np.ndarray) or isinstance(station_reference, list), 'Station reference must be passed as a string, list or np.ndarray'

    if isinstance(station_reference, str):
        station_reference = [station_reference]
    
    value_list = []
    dateTime_list = []
    lat_list = []
    long_list = []
    parameter_list = []

    for j in station_reference:
        try:
            df_live = pd.read_json(f'https://environment.data.gov.uk/flood-monitoring/id/stations/{j}')
        except:
            print(f' station reference {j} does not exist live')
            continue
            

        station_info = df_live.loc['measures', 'items']
        
        if isinstance(station_info, list):
            station_info = station_info[0]
        
        assert  isinstance(station_info, dict), f'{j} has a different format'
        
        if not isinstance(station_info.get('latestReading'), dict):
            value =  'Unavailable'
            parameter =  'Unavailable'
            lat = 'Unavailable'
            long = 'Unavailable'
            
        else:
            value = station_info.get('latestReading').get('value')
            value_list.append(value)
        
            dateTime = station_info.get('latestReading').get('dateTime')
            dateTime_list.append(dateTime)

            parameter = station_info.get('parameter')
            parameter_list.append(parameter)
            
        if 'lat' in df_live.index:
            lat = df_live.loc['lat', 'items']
            lat_list.append(lat)
        else:
            lat =  'Unavailable'
            
        if 'long' in df_live.index:  
            long = df_live.loc['long', 'items']
            long_list.append(long)
        else:
            long = 'Unavailable'
        

    station_data = pd.DataFrame(data= dateTime_list, columns=['dateTime'])
    station_data ['latitude'] = lat_list
    station_data ['longitude'] = long_list
    station_data ['parameter'] = parameter_list
    station_data ['value'] = value_list
   

    return station_data
    
    

