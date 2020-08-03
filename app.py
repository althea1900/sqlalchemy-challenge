import numpy as np

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
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of dates and prcp data"""
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date.between('2016-08-23', '2017-08-23'))

    # Create dictionary
    percipitation_data = []
    for date, prcp in results:
        dict = {}
        dict[date] = prcp
        percipitation_data.append(dict)

    session.close()

    return jsonify(percipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query for all station names.
    results = session.query(station.station, station.name).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    session = Session(engine)

    #query for all station names.
    active_stations = session.query(measurement.station, func.count(measurement.date)).group_by(measurement.station).\
    order_by(func.count(measurement.date).desc()).all()

    most_active_station = active_stations[0]

    active_station_data = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.station==(most_active_station[0])).all()

    session.close()

    return jsonify(active_station_data)

if __name__ == '__main__':
    app.run(debug=True)