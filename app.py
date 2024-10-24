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