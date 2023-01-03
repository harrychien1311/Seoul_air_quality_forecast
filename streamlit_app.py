import streamlit as st
import hopsworks
import pickle
import pandas as pd
import numpy as np
#import folium
#from streamlit_folium import st_folium, folium_static
import json
import time
from datetime import timedelta, datetime
#from branca.element import Figure

#from functions import decode_features, get_model

# Loading the trained model
pickle_in = open('xgb.pkl', 'rb')
model = pickle.load(pickle_in)
#@st.cache()
def collect_data():
    progress_bar = st.sidebar.header('⚙️ Working Progress')
    progress_bar = st.sidebar.progress(0)
    st.write(36 * "-")
    fancy_header('\n📡 Connecting to Hopsworks Feature Store...')
    project = hopsworks.login()
    fs = project.get_feature_store()
    st.write("Successfully connected!✔️")
    progress_bar.progress(20)
    st.write(36 * "-")
    fancy_header('\n☁️ Getting batch data from Feature Store...') 
    air_quality_data = fs.get_feature_group(
        name = "air_quality",
        version = 7
    )
    fancy_header('\n☁️ Successfully Got batch data from Feature Store!')
    air_quality_dataframe = air_quality_data.read(dataframe_type = "pandas")
    progress_bar.progress(100) 
    return air_quality_dataframe

def preprocess_data(df):
    # Select 5 newest days in the air quality data
    df_selected = df.drop("date", axis = 1)
    df_selected = df_selected.tail(6)
    # Flatten dataframe
    return np.expand_dims(df_selected.to_numpy().flatten(), axis = 0)

def predict(data):
    return model.predict(data)


def fancy_header(text, font_size=24):
    res = f'<span style="color:#ff5f27; font-size: {font_size}px;">{text}</span>'
    st.markdown(res, unsafe_allow_html=True )

def main():
    st.title('⛅️Seoul Air Quality Prediction🌩')
    df = collect_data()
    col1, col2, col3, col4, col5, col6 = st.columns(spec=6, gap="large")
    with col1:
        st.header(":blue[Air quality for] :green[{}]".format(pd.to_datetime(df.iloc[-5]["date"]).strftime('%d-%m-%y')))
        st.metric(label = "PM25", value = df.iloc[-5]["pm25"])
        st.metric(label = "PM10", value = df.iloc[-5]["pm10"])
        st.metric(label = "O3", value = df.iloc[-5]["o3"])
        st.metric(label = "no2", value = df.iloc[-5]["no2"])
        st.metric(label = "SO2", value = df.iloc[-5]["so2"])
        st.metric(label = "CO", value = df.iloc[-5]["co"])
    with col2:
        st.header(":blue[Air quality for] :green[{}]".format(pd.to_datetime(df.iloc[-4]["date"]).strftime('%d-%m-%y')))
        st.metric(label = "PM25", value = df.iloc[-4]["pm25"])
        st.metric(label = "PM10", value = df.iloc[-4]["pm10"])
        st.metric(label = "O3", value = df.iloc[-4]["o3"])
        st.metric(label = "no2", value = df.iloc[-4]["no2"])
        st.metric(label = "SO2", value = df.iloc[-4]["so2"])
        st.metric(label = "CO", value = df.iloc[-4]["co"])
    with col3:
        st.header(":blue[Air quality for] :green[{}]".format(pd.to_datetime(df.iloc[-3]["date"]).strftime('%d-%m-%y')))
        st.metric(label = "PM25", value = df.iloc[-3]["pm25"])
        st.metric(label = "PM10", value = df.iloc[-3]["pm10"])
        st.metric(label = "O3", value = df.iloc[-3]["o3"])
        st.metric(label = "no2", value = df.iloc[-3]["no2"])
        st.metric(label = "SO2", value = df.iloc[-3]["so2"])
        st.metric(label = "CO", value = df.iloc[-3]["co"])
    with col4:
        st.header(":blue[Air quality for] :green[{}]".format(pd.to_datetime(df.iloc[-2]["date"]).strftime('%d-%m-%y')))
        st.metric(label = "PM25", value = df.iloc[-2]["pm25"])
        st.metric(label = "PM10", value = df.iloc[-2]["pm10"])
        st.metric(label = "O3", value = df.iloc[-2]["o3"])
        st.metric(label = "no2", value = df.iloc[-2]["no2"])
        st.metric(label = "SO2", value = df.iloc[-2]["so2"])
        st.metric(label = "CO", value = df.iloc[-2]["co"])
    with col5:
        st.header(":blue[Air quality for] :green[{}]".format(pd.to_datetime(df.iloc[-1]["date"]).strftime('%d-%m-%y')))
        st.metric(label = "PM25", value = df.iloc[-1]["pm25"])
        st.metric(label = "PM10", value = df.iloc[-1]["pm10"])
        st.metric(label = "O3", value = df.iloc[-1]["o3"])
        st.metric(label = "no2", value = df.iloc[-1]["no2"])
        st.metric(label = "SO2", value = df.iloc[-1]["so2"])
        st.metric(label = "CO", value = df.iloc[-1]["co"])
    
    if st.button('Forecast the air quality for the next day'):
        data_array = preprocess_data(df)
        predicted_result = predict(data_array)
        col6.header(":blue[Air quality for tomorrow]")
        col6.metric(label = "PM25" , value = predicted_result[0][0])
        col6.metric(label = "PM10" , value = predicted_result[0][1])
        col6.metric(label = "O3" , value = predicted_result[0][2])
        col6.metric(label = "no2" , value = predicted_result[0][3])
        col6.metric(label = "SO2" , value = predicted_result[0][4])
        col6.metric(label = "CO" , value = predicted_result[0][5])

    else:
        col6.header(":blue[Air quality for tomorrow]")
    st.map(pd.DataFrame(zip([37.566535], [126.9779692]), columns = ['lat', 'lon']))
if __name__=='__main__':
    main()




