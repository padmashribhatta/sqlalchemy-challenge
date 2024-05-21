# Import the dependencies.
import numpy as np

import warnings
warnings.filterwarnings('ignore', message='The .reflect')

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy import func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################


engine = create_engine(r"sqlite:///Resources/hawaii.sqlite")

meta=MetaData()
meta.reflect(bind=engine)
print(meta.tables.keys())


Measurement = meta.tables["measurement"]
Station = meta.tables["station"]

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables

Base.prepare(engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Create our session (link) from Python to the DB

app = Flask(__name__)

#################################################
# Flask Setup
#################################################


engine = create_engine(r"sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/start'>/api/v1.0/start</a><br/>"
        f"<a href='/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"
    )


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last date in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary of precipitation data
    precip_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations_data = session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(stations_data))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last date in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the most active station for the last 12 months of temperature data
    results = session.query(Measurement.tobs)\
        .filter(Measurement.date >= one_year_ago)\
        .filter(Measurement.station == "USC00519281").all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end=None):
    if end:
        # Query TMIN, TAVG, and TMAX for the date range
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        # Query TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start).all()

    # Create a dictionary of results
    temp_dict = {"minimum temperature": results[0][0],
                 "average temperature": results[0][1],
                 "maximum temperature": results[0][2]}

    return jsonify(temp_dict)
app.run()









