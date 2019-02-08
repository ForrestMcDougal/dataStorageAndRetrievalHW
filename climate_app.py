import datetime as dt
import numpy as np
import os

from flask import Flask, jsonify, render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


@app.route("/")
@app.route("/index")
def welcome():
    """List all available api routes."""
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'surfs-up.jpeg')
    return render_template("index.html", user_image=full_filename)


@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_session = Session(engine)

    query = (Measurement.date, func.avg(Measurement.prcp))

    prcp = precipitation_session.query(*query). \
        group_by(Measurement.date).all()

    prcp_dict = dict()
    for p in prcp:
        prcp_dict[p[0]] = p[1]

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations_session = Session(engine)
    query = (Measurement.station, )
    station_info = stations_session.query(*query).\
        order_by(func.count(Measurement.station).desc()).\
        group_by(Measurement.station).all()
    
    all_stations = list(np.ravel(station_info))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    tobs_session = Session(engine)

    query = (Measurement.date, )

    last_day = tobs_session.query(*query).\
        order_by(Measurement.date.desc()).first()[0]
    
    last_day_dt = dt.datetime.strptime(last_day, '%Y-%m-%d').date()
    one_year_ago = last_day_dt - dt.timedelta(days=365)
    one_year_ago_str = str(one_year_ago)

    query = (Measurement.date, func.min(Measurement.tobs),
             func.avg(Measurement.tobs), func.max(Measurement.tobs))

    results = tobs_session.query(*query).\
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
    temps_session = Session(engine)

    query = (func.min(Measurement.tobs), func.avg(Measurement.tobs),
             func.max(Measurement.tobs))

    all_temps =  temps_session.query(*query).\
        filter(Measurement.date >= start).all()

    temps_list = list(np.ravel(all_temps))

    return jsonify(temps_list)


@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    temp_range_session = Session(engine)

    query = (func.min(Measurement.tobs), func.avg(Measurement.tobs),
             func.max(Measurement.tobs))
             
    temps_range = temp_range_session.query(*query).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    temp_range_list = list(np.ravel(temps_range))

    return jsonify(temp_range_list)


if __name__ == '__main__':
    app.run(debug=True)
