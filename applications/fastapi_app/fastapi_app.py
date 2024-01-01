from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import pandas as pd
import pickle
from data_preprocessing import *

app = FastAPI()

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/predict")
async def predict(request: Request):
    form = await request.form()
    
    airlines = {'Lufthansa': 19, 'TAROM': 24, 'Air France': 4, 'Wizz Air': 32, 'British Airways': 9, 'Tunisair': 28, 'Royal Air Maroc': 21, 'TAP Portugal': 23, 'Air Serbia': 6, 'ITA Airways': 15, 'AnadoluJet': 7, 'Turkish Airlines': 29, 'Iberia': 16, 'Aegean Airlines': 0, 'Pegasus Airlines': 20, 'Transavia France': 27, 'Egypt Air': 12, 'KLM': 17, 'Vueling': 31, 'LOT': 18, 'Austrian Airlines': 8, 'Air Algerie': 1, 'SWISS': 22, 'TUI Fly Belgium': 25, 'Air Europa': 3, 'Air Arabia Maroc': 2, 'easyJet': 33, 'CitizenPlane': 11, 'Transavia': 26, 'Brussels Airlines': 10, 'Volotea': 30, 'Eurowings': 13, 'FLYONE': 14, 'Air Malta': 5}
    seasons={'Autumn': 0, 'Spring': 1, 'Summer': 2, 'Winter': 3}
    arrival_times={'Late Night': 3, 'Afternoon': 0, 'Night': 5, 'Evening': 2, 'Morning': 4, 'Early Morning': 1}
    depature_times={'Afternoon': 0, 'Morning': 4, 'Evening': 2, 'Early Morning': 1, 'Late Night': 3, 'Night': 5}
    classes={'Economy': 1, 'Business': 0}
    
    
    airline = form["airline"]
    airline_encoded=airlines[airline]

    class_=form["class"]
    classes_encoded=classes[class_]  
    
    Total_stops = int(form['stops'])
    
    

    Source = form["Source"]
    sources = {
        'Casablanca': [1, 0, 0, 0],
        'Istanbul': [0, 1, 0, 0],
        'Paris': [0, 0, 1, 0],
        'Rome': [0, 0, 0, 1]
    }
    source_encoded = sources.get(Source, [0, 0, 0, 0])
    s_CMN, s_IST, s_PAR, s_ROM = source_encoded


    Destination = form["Destination"]
    destinations = {
        'Paris': [0, 0, 1, 0],
        'Casablanca': [1, 0, 0, 0],
        'Istanbul': [0, 1, 0, 0],
        'Rome': [0, 0, 0, 1]
    }
    destination_encoded = destinations.get(Destination, [0, 0, 0, 0])
    d_CMN, d_IST, d_PAR, d_ROM = destination_encoded
    
    dep_time = form['Dep_Time']

    month = int(pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").month)

    season=date_to_season2(month)
    season_encoded=seasons[season]
    Departure_hour = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").hour

    arrival_time = form['Arrival_Time']
    Arrival_hour = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").hour

    flight_duration = pd.to_datetime(arrival_time) - pd.to_datetime(dep_time)
    flight_duration_minutes = flight_duration.total_seconds() / 60
    
    arr_hour=categorize_time2(Arrival_hour)
    dep_hour=categorize_time2(Departure_hour)
    
    arrival_time_encoded=arrival_times[arr_hour]
    departure_time_encoded=depature_times[dep_hour]
    print([
        airline_encoded,
        flight_duration_minutes,
        Total_stops,
        classes_encoded,
        departure_time_encoded,
        arrival_time_encoded,
        season_encoded,
        s_CMN,
        s_IST,
        s_PAR,
        s_ROM,
        d_CMN,
        d_IST,
        d_PAR,
        d_ROM
        ])
    output = model.predict([[
        airline_encoded,
        flight_duration_minutes,
        Total_stops,
        classes_encoded,
        departure_time_encoded,
        arrival_time_encoded,
        season_encoded,
        s_CMN,
        s_IST,
        s_PAR,
        s_ROM,
        d_CMN,
        d_IST,
        d_PAR,
        d_ROM
        ]])

    return {"prediction": output.tolist()}

if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)






