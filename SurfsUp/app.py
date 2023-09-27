import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Values to use on queries
newest_date = dt.date(2017, 8, 23)
last_year = newest_date - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 1. Main route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Consult all precipitation values in last year<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Consult all available station names<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Consult temperature observations for last year of values from station USC00519281<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Consult by start date route. Format(YYY-MM-DD):<br/>"
        f"/api/v1.0/<br/>"
        f"<br/>"
        f"Consult by start and end date route. Format(YYYY-MM-DD/YYYY-MM-DD):<br/>"
        f"/api/v1.0/"
    )

# 2. Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and precipitation values from the dataset """
    # Query all precipitation values in last year
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all precipitation values
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# 3. Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset """
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

# 4. Temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset """
    # Query temperature observations for last year of values of station USC00519281
    results = session.query(Measurement.tobs).\
            filter(Measurement.station == "USC00519281",\
            Measurement.date >= last_year, ).all()
    
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

# 5. Statistics of temperature observations route by start date
@app.route("/api/v1.0/<start>")
def by_start_date(start):
    
    year = start[:4]
    month = start[5:7]
    day = start[8:10]
    
    date = dt.date(int(year), int(month), int(day))

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset """
    # Query temperature observations from start date specified
    sel = [func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]
    results = session.query(*sel).\
    filter(Measurement.date >= date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all precipitation values
    all_prcp = []
    for min_temp, max_temp, avg_temp in results:
        prcp_dict = {}
        prcp_dict["min temp"] = min_temp
        prcp_dict["max_temp"] = max_temp
        prcp_dict["avg_temp"] = avg_temp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# 6. Statistics of temperature observations route by start and end date
@app.route("/api/v1.0/<start>/<end>")
def by_start_end_date(start, end):
    
    year1 = start[:4]
    month1 = start[5:7]
    day1 = start[8:10]
    date1 = dt.date(int(year1), int(month1), int(day1))

    year2 = end[:4]
    month2 = end[5:7]
    day2 = end[8:10]
    date2 = dt.date(int(year2), int(month2), int(day2))

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset """
    # Query temperature observations from start date specified
    sel = [func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]
    results = session.query(*sel).\
    filter(Measurement.date >= date1, Measurement.date <= date2).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all precipitation values
    all_prcp = []
    for min_temp, max_temp, avg_temp in results:
        prcp_dict = {}
        prcp_dict["min temp"] = min_temp
        prcp_dict["max_temp"] = max_temp
        prcp_dict["avg_temp"] = avg_temp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

if __name__ == '__main__':
    app.run(debug=True)