import numpy as np
import pandas as pd
import datetime as dt
import sqlite3

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/Welcome')
def welcome():
    return (
        f"Available Routes for the Hawaii Climate Analysis:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end" 
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    # Create a dictionary from the row data and append to a list of all_precipitation

    year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date >= year_ago).all()
    
    session.close()

    all_precipitation = list(np.ravel(results))

    return jsonify(all_precipitation)

@app.route('/api/v1.0/stations')
def stations():

    stats=session.query(Measurement.station).all()
    for stat in stats:
        if stat not in stationList:
            stationList.append(stat)
    
    return jsonify(stationList)

@app.route('/api/v1.0/tobs')
def tobs():

    year_agoT=dt.date(2017,8,23) - dt.timedelta(days=365)

    observations=session.query(Measurement.date,Measurement.tobs).\
                    filter(Measurement.date >= year_ago).all()
    return jsonify(observations)

@app.route('/api/v1.0/<start>/<end>')
def api_dates(year, month, day):

    def calc_temps(start_date, end_date):
        start_date=dt.datetime(int(year), int(month), int(day))
        end_date=dt.datetime(int(year), int(month), int(day))
    
        dateQuery = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()
        return jsonify([dateQuery])


if __name__ == '__main__':
    app.run(debug=True)