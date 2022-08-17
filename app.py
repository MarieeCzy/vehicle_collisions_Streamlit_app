from json import load
from re import U
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = (
    'data/Motor_Vehicle_Collisions_-_Crashes.csv'
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("#### This application is a Streamlit dashboard that can be used"
            " to analyze motor vehicle collisions in NYC.")

#function loading our data from file
#parameter - nrows
#@st.cache - avoid computing changes every time app is rerun

@st.cache(persist=True)
def load_data(nrows= 1000):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH TIME', 'CRASH DATE']])
    data.dropna(subset=['LONGITUDE', 'LATITUDE'], inplace= True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace= True)
    data.rename(columns= {'crash time_crash date': 'date/time', 'number of persons injured': 'injured_persons'}, inplace= True)
    return data

#slider1
nrows_ = st.sidebar.slider("How many accidents you want to analyze?", 0, 1000000, 150000)
data = load_data(nrows_)
original_data = data

#slider2
st.header('Where are the most people injured in NYC?')
injured_people = st.sidebar.slider("Number of persons injured in vehicle collisions", 0, 19, 5)
#create map
st.map(data.query(f"injured_persons >= {injured_people}")[["latitude", "longitude"]].dropna(how="any"))

#slider3
st.header('How many collisions occur during a given time of day?')
hour = st.sidebar.slider('Hour to look at',0 , 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown('Vehicle collisions between %i:00 and %i:00' % (hour, (hour +1)))
#midpoint = (np.average(data['latitude']), np.average(data['longitude']))

#3d map
def show_on_map(lattitude, longitude, data, radius):
    st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v9",
    initial_view_state={
        'latitude': lattitude,
        'longitude': longitude,
        'zoom': 10,
        'pitch': 50,   
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=['longitude', 'latitude'],
            radius=radius,
            extruded=True,
            pickable=True,
            elevation_scale=11,
            elevation_range=[0, 1500],
        ),
    ],
))

NYC_latitude = 40.730610
NYC_longitude = -73.935242

show_on_map(NYC_latitude, NYC_longitude, 
            data[['date/time', 'latitude', 'longitude']], 
            100)

#---plot---
st.subheader('Breakdown by minute between %i:00 and %i:00' % (hour, (hour+1)%24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
#accidents
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
#create new data frame
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
#plot fig and write on web
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerous street by affected type")
select = st.selectbox("Affected type of people", ['Pedestrians', 'Cyclists', 'Motorists'])
select_type = st.selectbox("Result of accident", ['Injured', 'Killed'])

original_data.rename(columns= {'number of pedestrians injured': 'injured_pedestrians',
                               'on street name': 'on_street_name',
                               'number of cyclist injured': 'injured_cyclists',
                               'number of motorist injured': 'injured_motorists',
                               'number of pedestrians killed': 'killed_pedestrians',
                               'number of cyclist killed': 'killed_cyclists',
                               'number of motorist killed': 'killed_motorists'}, inplace=True)

if select == 'Pedestrians':
    
    if select_type == "Injured":
        pedestrians_injured = original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians", "longitude", "latitude"]].sort_values(by=["injured_pedestrians"], ascending=False).dropna(how='any')[:5]
        st.write(pedestrians_injured)
        st.write(show_on_map(pedestrians_injured['latitude'].iloc[0],
                             pedestrians_injured['longitude'].iloc[0],
                             pedestrians_injured,
                             150))
    
    else:
        pedestrians_killed = original_data.query("killed_pedestrians >= 1")[["on_street_name", "killed_pedestrians", "longitude", "latitude"]].sort_values(by=["killed_pedestrians"], ascending=False).dropna(how='any')[:5]
        st.write(pedestrians_killed)
        st.write(show_on_map(pedestrians_killed['latitude'].iloc[0],
                             pedestrians_killed['longitude'].iloc[0],
                             pedestrians_killed,
                             200))

elif select == 'Cyclists':
    if select_type == "Injured":
        cyclists_injured = original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists", "longitude", "latitude"]].sort_values(by=["injured_cyclists"], ascending=False).dropna(how="any")[:5]
        st.write(cyclists_injured)
        st.write(show_on_map(cyclists_injured['latitude'].iloc[0],
                             cyclists_injured['longitude'].iloc[0],
                             cyclists_injured,
                             150))
    
    else:
        cyclists_killed = original_data.query("killed_cyclists >= 1")[["on_street_name", "killed_cyclists", "longitude", "latitude"]].sort_values(by=["killed_cyclists"], ascending=False).dropna(how='any')[:5]
        st.write(cyclists_killed)
        st.write(show_on_map(cyclists_killed['latitude'].iloc[0],
                             cyclists_killed['longitude'].iloc[0],
                             cyclists_killed,
                             150))
        
else:
    if select_type == "Injured":
        motorists_injured = original_data.query('injured_motorists >=1')[["on_street_name", "injured_motorists", "longitude", "latitude"]].sort_values(by=["injured_motorists"], ascending=False).dropna(how="any")[:5]
        st.write(motorists_injured)
        st.write(show_on_map(motorists_injured['latitude'].iloc[0],
                             motorists_injured['longitude'].iloc[0],
                             motorists_injured,
                             200))
        
    else:
        motorists_killed = original_data.query("killed_motorists >= 0")[["on_street_name", "killed_motorists", "longitude", "latitude"]].sort_values(by=["killed_motorists"], ascending=False).dropna(how='any')[:5]
        st.write(motorists_killed)
        st.write(show_on_map(motorists_killed['latitude'].iloc[0],
                             motorists_killed['longitude'].iloc[0],
                             motorists_killed,
                             200))
    
print(original_data.columns)
if st.checkbox('Show Raw Data', True):
    st.subheader('Raw data')
    st.write(data)

#to run our streamlit app- import library streamlit and enter in terminal: streamlit run app.py
