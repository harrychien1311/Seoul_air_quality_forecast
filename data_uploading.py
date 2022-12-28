import pandas as pd
import hopsworks
from datetime import datetime


def process_data():
    data = pd.read_csv("data/seoul-air-quality.csv")
    data["date"] = pd.to_datetime(data["date"])
    data.sort_values(by = 'date', ascending = True, inplace = True)
    data.replace(" ", "0", inplace = True)
    feature_dict = {" pm25":"pm25", " pm10":"pm10", " o3":"o3", " no2":"no2", " so2":"so2", " co":"co"}
    data.rename(columns = feature_dict, inplace = True)
    feature_list = ["pm25","pm10", "o3", "no2", "so2", "co"]
    for feature in feature_list:
        data[feature] = data[feature].astype(float)
    data.date = data.date.astype(int)
    return data
def upload(data):
    project = hopsworks.login(api_key_value = "rmUyQzceRAvPvA54.lVao1a8UeILkS4HQfUekvBcMZTqk2Au1kGQzGHidMdOtluwklOpIuivKfBoPh7dd")
    fs = project.get_feature_store()
    air_fg = fs.get_feature_group(
        name="air_quality",
        version=7,
        #description="Seoul air quality data",
        #primary_key = ["time"],
        #event_time="time",
        #online_enabled=True,
        #statistics_config={"enabled": True, "histograms": True, "correlations": True},
    )
    air_fg.insert(data)

if __name__=="__main__":
    data = process_data()
    upload(data)
