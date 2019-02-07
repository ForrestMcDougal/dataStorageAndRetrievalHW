import datetime as dt
import numpy as np

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    query = (Measurement.station, )
    station_info = session.query(*query).\
        order_by(func.count(Measurement.station).desc()).\
        group_by(Measurement.station).all()
    
    all_stations = list(np.ravel(station_info))

    return jsonify(all_stations)


@app.route("/api/v1.0/<start>")
def temps(start):
    session = Session(engine)
    query = (func.min(Measurement.tobs), func.avg(Measurement.tobs),
             func.max(Measurement.tobs))
    all_temps =  session.query(*query).\
        filter(Measurement.date >= start).all()

    temps_list = list(np.ravel(all_temps))

    return jsonify(temps_list)


@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    session = Session(engine)
    query = (func.min(Measurement.tobs), func.avg(Measurement.tobs),
             func.max(Measurement.tobs))
    temps_range = session.query(*query).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    temp_range_list = list(np.ravel(temps_range))

    return jsonify(temp_range_list)


if __name__ == '__main__':
    app.run(debug=True)