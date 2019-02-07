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


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_day = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()[0]
    
    last_day_dt = dt.datetime.strptime(last_day, '%Y-%m-%d').date()
    one_year_ago = last_day_dt - dt.timedelta(days=365)
    one_year_ago_str = str(one_year_ago)

    query = (Measurement.date, func.min(Measurement.tobs),
             func.avg(Measurement.tobs), func.max(Measurement.tobs))

    results = session.query(*query).\
        filter(Measurement.date > one_year_ago_str).\
        order_by(Measurement.date).\
        group_by(Measurement.date).all()
    
    tobs = []
    for result in results:
        temp_tobs = dict()
        temp_tobs['date'] = result[0]
        temp_tobs['min_temp'] = result[1]
        temp_tobs['avg_temp'] = round(result[2])
        temp_tobs['max_temp'] = result[3]
        tobs.append(temp_tobs)

    return jsonify(tobs)


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