# Import the dependencies.
import numpy as np
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

#################################################
# Database Setup
#################################################

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///C:/Git Repos/new_hawaii.sqlite")

# Define the base
Base = declarative_base()

# Define the Measurement class
class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)

# Define the Station class
class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

# Create a session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    """Home route listing available API routes"""
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return the precipitation data for the last 12 months"""
    # Calculate the date one year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(str(last_date), '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query for the precipitation data for the last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_dict = {str(date): prcp for date, prcp in precipitation_data}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
    """Return a list of all station names"""
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return temperature observations for the most active station for the last year"""
    # Calculate the date one year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(str(last_date), '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the temperature observations for the most active station
    results = session.query(Measurement.tobs).filter(
        Measurement.station == 'USC00519281',
        Measurement.date >= one_year_ago
    ).all()

    tobs_list = [temp[0] for temp in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temperature_stats(start, end=None):
    """Return min, avg, and max temperatures from a start date or start-end range"""
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)





 #Route: 
 @app.route('/')
#Description: This is the root route, which serves as the homepage of the Flask API. It provides a list of all available routes in the application.
#How to Access: Visit http://127.0.0.1:5000/ in a browser. This will display a welcome message along with the list of all the available routes for the API.

#Route: 
@app.route('/api/v1.0/precipitation')
#Description: This route returns the precipitation data for the last 12 months. It calculates the date one year ago from the most recent date in the dataset and retrieves all precipitation data from that date onward.
#How to Access: Visit http://127.0.0.1:5000/api/v1.0/precipitation in a browser. The response will be a JSON object containing the date as the key and precipitation as the value for each entry.

#Route: 
@app.route('/api/v1.0/stations')
#Description: This route returns a JSON list of all the weather stations in the database.
#How to Access: Visit http://127.0.0.1:5000/api/v1.0/stations in a browser. The response will be a JSON list containing the station IDs of all stations.


#Route: @app.route('/api/v1.0/tobs')
#Description: This route returns a JSON list of temperature observations (TOBS) for the most active station for the previous year.
#How to Access: Visit http://127.0.0.1:5000/api/v1.0/tobs in a browser. The response will be a JSON list of temperature observations for the most active weather station.

#Routes:
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
#Description: These routes return a JSON list containing the minimum, average, and maximum temperatures for a specified start date or for a date range from start to end.
#How to Access:
#Visit http://127.0.0.1:5000/api/v1.0/2017-01-01 to get the temperature statistics from January 1, 2017, to the end of the dataset.
#Visit http://127.0.0.1:5000/api/v1.0/2017-01-01/2017-12-31 to get the temperature statistics from January 1, 2017, to December 31, 2017.
