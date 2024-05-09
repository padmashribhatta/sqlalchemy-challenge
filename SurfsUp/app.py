# Import the dependencies.
import numpy as np
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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Create our session (link) from Python to the DB

app = Flask(__name__)

#################################################
# Flask Setup
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    prcp_dict = {date: prcp for date, prcp in prcp_results}
    return jsonify(prcp_dict)

# define stations route
@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()
    stations_list = list(np.ravel(station_results))
    return jsonify(stations=stations_list)

# define temperature observations route for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    temp_results = session.query(Measurement.date, Measurement.tobs).\
                   filter(Measurement.station == most_active_station).\
                   filter(Measurement.date >= last_year).all()
    temp_list = list(np.ravel(temp_results))
    return jsonify(temps=temp_list)

# define start and start/end date route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end=None):
    if end:
        temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                       filter(Measurement.date >= start).\
                       filter(Measurement.date <= end).all()
    else:
        temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                       filter(Measurement.date >= start).all()
    temp_list = list(np.ravel(temp_results))
    return jsonify(min=temp_list[0], avg=temp_list[1], max=temp_list[2])

# run the app
if __name__ == "__main__":
    app.run()


#################################################
# Flask Routes
#################################################
