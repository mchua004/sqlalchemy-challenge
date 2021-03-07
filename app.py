import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return the precipitation scores for the last year of data"""
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
                  group_by(Measurement.date).\
                  filter(Measurement.date.between('2016-08-23', '2017-08-23'))
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of precipitation_scores
    precipitation_scores = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_scores.append(precipitation_dict)

    return jsonify(precipitation_scores)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return the list of stations in the dataset"""
    # Perform a query to retrieve the stations in the dataset
    results = session.query(Measurement.station.distinct()).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of stations
    station_list = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station
        station_list.append(station_dict)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return the dates and temperature observations of the most active station for the last year of data"""
    # Perform a query to retrieve the dates amd temperature observations of the most active station for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).\
                  filter(Measurement.station == 'USC00519281').\
                  filter(Measurement.date.between('2016-08-23', '2017-08-23'))
    
    session.close()

    # Create a dictionary from the row data and append to a list of temperature observations for the last year
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Ask for the year, month, and date for the 'start' date
    year = input('Enter the year of the start date:' )
    month = input('Enter the month of the start date:' )
    day = input('Enter the day of the start date:' )
    
    start_date = dt.date(int(year), int(month), int(day))
    
    """Return the dates and temperature observations of the most active station for the last year of data"""
    # Perform a query to retrieve the minimum temperature, average temperature, and maximum temperature for the given start date
    results = session.query(func.min(Measurement.tobs).label("TMIN"), func.max(Measurement.tobs).label("TMAX"), func.avg(Measurement.tobs).label("TAVG")).\
                  filter(Measurement.date == start_date)
    
    session.close()

    # Create a dictionary from the row data and append to the list containing the min, max, and avg temp for the start date
    start_list = []
    for TMIN, TMAX, TAVG in results:
        start_dict = {}
        start_dict["TMIN"] = TMIN
        start_dict["TMAX"] = TMAX
        start_dict["TAVG"] = TAVG
        start_list.append(start_dict)

    return jsonify(start_list)


@app.route("/api/v1.0/start_end")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Ask for the year, month, and date for the 'start' date
    start_year = input('Enter the year of the start date:' )

    start_month = input('Enter the month of the start date:' )

    start_day = input('Enter the day of the start date:' )
    


    #Ask for the year, month, and date for the 'end' date
    end_year = input('Enter the year of the end date:' )

    end_month = input('Enter the month of the end date:' )
 
    end_day = input('Enter the day of the end date:' )
    
    start_date = dt.date(int(start_year), int(start_month), int(start_day))
    end_date = dt.date(int(end_year), int(end_month), int(end_day))
    
    """Return the dates and temperature observations of the most active station for the last year of data"""
    # Perform a query to retrieve the minimum temperature, average temperature, and maximum temperature for dates between the start date and end date inclusive
    results = session.query(func.min(Measurement.tobs).label("TMIN"), func.max(Measurement.tobs).label("TMAX"), func.avg(Measurement.tobs).label("TAVG")).\
                  filter(Measurement.date.between(start_date, end_date))
    
    session.close()

    # Create a dictionary from the row data and append to a list containing the min, max, and, avg temp between the start and end date
    start_end_list = []
    for TMIN, TMAX, TAVG in results:
        start_end_dict = {}
        start_end_dict["TMIN"] = TMIN
        start_end_dict["TMAX"] = TMAX
        start_end_dict["TAVG"] = TAVG
        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)

