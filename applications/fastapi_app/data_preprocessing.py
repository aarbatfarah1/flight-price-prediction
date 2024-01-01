import pandas as pd
from datetime import datetime
import re
from sklearn.utils import shuffle


def clean_arrival_time(arrival_time):
    if '+' in arrival_time:
        return arrival_time.split('+')[0]
    else:
        return arrival_time
    

def convert_stops_to_numeric(df, column_name):
    mapping_dict = {value: index for index, value in enumerate(df[column_name].unique())}

    df[column_name] = df[column_name].replace(mapping_dict)

    return df

def date_to_season(date_str):
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    month = date_object.month

    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Autumn'
    else:
        return 'Winter'
    
def date_to_season2(month):

    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Autumn'
    else:
        return 'Winter'
def df_to_season(df):
    seasons=[]
    for index, row in df.iterrows():
        # Access individual elements using column names
        row['Season'] = date_to_season(row['Date'])
        seasons.append(row['Season'])
    df['Season']=seasons


def categorize_time(hour):
    # Split the string using ":" as the delimiter
    hours, minutes = map(int, hour.split(':'))
    # Extract the hour part as an integer
    hour_as_int = int(hours)
    if 4 <= hour_as_int < 7:
        return "Early Morning"
    elif 7 <= hour_as_int < 12:
        return "Morning"
    elif 12 <= hour_as_int < 17:
        return "Afternoon"
    elif 17 <= hour_as_int < 20:
        return "Evening"
    elif 20 <= hour_as_int < 24:
        return "Night"
    else:
        return "Late Night"
    
def categorize_time2(hour):
    hour_as_int = int(hour)
    if 4 <= hour_as_int < 7:
        return "Early Morning"
    elif 7 <= hour_as_int < 12:
        return "Morning"
    elif 12 <= hour_as_int < 17:
        return "Afternoon"
    elif 17 <= hour_as_int < 20:
        return "Evening"
    elif 20 <= hour_as_int < 24:
        return "Night"
    else:
        return "Late Night"






