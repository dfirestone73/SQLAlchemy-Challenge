import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
def home():
    return (
        f"Available Routes:<br/>"
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

    results = session.query(Measurement.date, Measurement.prcp).all()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    stats=session.query(Measurement.station).all()
    for stat in stats:
    if stat not in stationList:
        stationList.append(stat)
    
    return jsonify(stationList)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

@app.route('/api/v1.0/<start>')
def start():
    session = Session(engine)

@app.route('/api/v1.0/<start>/<end>')
def end():
    session = Session(engine)




@app.route('/api')
def api_route():
    return render_template('index.html')

@app.route('/api/<year>')
def api_year(year):
    date=dt.datetime(int(year), 1, 1)
    return jsonify([date])

if __name__ == '__main__':
    app.run(debug=True)