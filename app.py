import numpy as np
import pandas as pd
import datetime as dt
import sqlite3

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

app = Flask(__name__)
# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)


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
        f"/api/v1.0/startend" 
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    
    year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date >= year_ago).all()
    
    all_precipitation = list(np.ravel(results))

    return jsonify(all_precipitation)

@app.route('/api/v1.0/stations')
def stations():

    stationList=[]

    stats=session.query(Measurement.station).all()
    for stat in stats:
        if stat not in stationList:
            stationList.append(stat)
    
    return jsonify(stationList)

@app.route('/api/v1.0/tobs')
def tobs():

    year_agoT=dt.date(2017,8,23) - dt.timedelta(days=365)

    observations=session.query(Measurement.date,Measurement.tobs).\
                    filter(Measurement.date >= year_agoT).all()
    
    return jsonify(observations)

@app.route('/api/v1.0/<start>')
def single_date(startdate):

    startQuery = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
        func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) == startdate).all()
        
    return jsonify(startQuery)

@app.route('/api/v1.0/<start><end>')
def api_dates(start, end):

    dateQuery = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()
        
    return jsonify(dateQuery)


if __name__ == '__main__':
    app.run(debug=True)