import streamlit as st
import requests
from datetime import datetime
from streamlit.components.v1 import html

# Streamlit app code
def main():
    st.image("background-2.jpg", use_column_width=True)
    st.title("Flight Price Prediction")

    # Input form
    with st.form("flight_form"):
        dep_date = st.date_input("Departure Date", value=datetime.now().date())
        dep_time = st.time_input("Departure Time", value=datetime.now().time())
        arrival_date = st.date_input("Arrival Date", value=datetime.now().date())
        arrival_time = st.time_input("Arrival Time", value=datetime.now().time())
        stops = st.radio("Number of Stops", [0, 1, 2, 3], index=0)

        airlines = {'Lufthansa': 19, 'TAROM': 24, 'Air France': 4, 'Wizz Air': 32, 'British Airways': 9, 'Tunisair': 28, 'Royal Air Maroc': 21, 'TAP Portugal': 23, 'Air Serbia': 6, 'ITA Airways': 15, 'AnadoluJet': 7, 'Turkish Airlines': 29, 'Iberia': 16, 'Aegean Airlines': 0, 'Pegasus Airlines': 20, 'Transavia France': 27, 'Egypt Air': 12, 'KLM': 17, 'Vueling': 31, 'LOT': 18, 'Austrian Airlines': 8, 'Air Algerie': 1, 'SWISS': 22, 'TUI Fly Belgium': 25, 'Air Europa': 3, 'Air Arabia Maroc': 2, 'easyJet': 33, 'CitizenPlane': 11, 'Transavia': 26, 'Brussels Airlines': 10, 'Volotea': 30, 'Eurowings': 13, 'FLYONE': 14, 'Air Malta': 5}
        airline = st.selectbox("Airline", list(airlines.keys()), index = 0)
        
        classes={'Economy': 1, 'Business': 0}
        class_=st.selectbox("Class",list(classes.keys()), index = 0)
        
        sources ={
        'Casablanca': [1, 0, 0, 0],
        'Istanbul': [0, 1, 0, 0],
        'Paris': [0, 0, 1, 0],
        'Rome': [0, 0, 0, 1]
        }
        destinations ={
        'Paris': [0, 0, 1, 0],
        'Casablanca': [1, 0, 0, 0],
        'Istanbul': [0, 1, 0, 0],
        'Rome': [0, 0, 0, 1]
        }
        
        source = st.selectbox("Source",list(sources.keys()) , index = 0)
        destination = st.selectbox("Destination",list(destinations.keys()) , index = 0)

        submitted = st.form_submit_button("Predict")

    # Make API request to FastAPI
    if submitted:
        dep_datetime = datetime.combine(dep_date, dep_time).strftime("%Y-%m-%dT%H:%M")
        arrival_datetime = datetime.combine(arrival_date, arrival_time).strftime("%Y-%m-%dT%H:%M")

        payload = {
            "Dep_Time": dep_datetime,
            "Arrival_Time": arrival_datetime,
            "stops": stops,
            "airline": airline,
            "Source": source,
            "Destination": destination,
            "class":class_
        }

        response = requests.post("http://backend.docker:8000/predict", data=payload)
    
        if response.status_code == 200:
            prediction_rf = response.json()["prediction"][0]
            st.success(f"Predicted Flight Price: {prediction_rf:.2f} MAD")
        else:
            st.error("Error occurred during prediction.")



if __name__ == "__main__":
    main()