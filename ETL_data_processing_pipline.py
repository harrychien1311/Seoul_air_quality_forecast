from prefect import task, flow
import json
from prefect.task_runners import SequentialTaskRunner
import pandas as pd
import numpy
import os
import hopsworks
from datetime import datetime, date

@task(retries = 3, retry_delay_seconds = 10)
def extract(url):
    return pd.read_json(url)

# Transform data to dataframe
@task
def transform(data):
    all_rows = numpy.empty(shape=(1,12)) 
    for i, row in enumerate(data['data']['iaqi']):
        all_rows[0][i] = (data['data']['iaqi'][row]['v'])
    df = pd.DataFrame(data = all_rows, columns = ['co', 'h', 'no2', 'o3', 'p', 'pm10', 'pm25', 'r', 'so2', 't', 'w', 'wd'])
    df['date'] = pd.to_datetime(date.today())
    df['date'] = df['date'].astype(int)
    df.drop(["h", "p", "r", "t", "w", "wd"], axis = 1, inplace = True)
    return df

# Uploading the data to Hopsworks Feature Store
@task
def load(dataframe):
    # Create a hopswork connection
    project = hopsworks.login(api_key_value = 'rmUyQzceRAvPvA54.lVao1a8UeILkS4HQfUekvBcMZTqk2Au1kGQzGHidMdOtluwklOpIuivKfBoPh7dd')
    fs = project.get_feature_store() #Get a feature store object
    # Get the created feature group with name and version
    air_fg = fs.get_feature_group(
        name="air_quality",
        version=7,
    )
    air_fg.insert(dataframe)

# Air quality data collection flow
@flow(name="Air quality ETL flow",
task_runner=SequentialTaskRunner())
def air_quality_data_collect(url):
    data = extract(url)
    df = transform(data)
    load(df)

#call the flow
if __name__== "__main__":
    air_quality_data_collect("https://api.waqi.info/feed/here/?token=ff91733805cf1cee918647f1cecedfcfaa458be0")
