import json
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime


app = Flask(__name__)

# sqlite path
sqlite_path = 'sqlite:///hawaii.sqlite'
engine = create_engine(sqlite_path)
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


@app.route('/')
def hello_world():  # put application's code here
    api_list = f"/api/v1.0/precipitation<br/>" \
        f"/api/v1.0/stations<br/>" \
        f"/api/v1.0/tobs<br/>" \

    return api_list

# /api/v1.0/precipitation


@app.route('/api/v1.0/precipitation')
def precipitation():
    # start session
    session = Session(engine)
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    query_results = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    last_12_month = query_results[0]
    last_date = datetime.datetime.strptime(last_12_month, '%Y-%m-%d').date()
    time_range = last_date - datetime.timedelta(days=365)

    ans = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= time_range).all()
    # convert it to json first
    json_results = []
    for result in ans:
        json_results.append({result.date: result.prcp})
    # close session
    session.close()
    return jsonify(json_results)


# /api/v1.0/stations
@app.route('/api/v1.0/stations')
def station():
    # start session
    session = Session(engine)
    # Return a JSON list of stations from the dataset.
    query_results = session.query(Station.station).all()
    # convert it to json first
    json_results = []
    for result in query_results:
        json_results.append(result.station)
    # close session
    session.close()
    return jsonify(json_results)

# /api/v1.0/tobs


@app.route('/api/v1.0/tobs')
def tobs():
    # start session
    session = Session(engine)
    # Return a JSON list of Temperature Observations (tobs) for the previous year
    stations = session.query(func.count(Measurement.station).label(
        'count'), Measurement.station, Station.name)
    filtered_station = stations.filter(Station.station == Measurement.station)
    group_by_station = filtered_station.group_by(Measurement.station).order_by(
        func.count(Measurement.station).desc()).all()

    # convert it to json first
    json_results = []
    for result in group_by_station:
        temp_dict = {}
        temp_dict["count"] = result.count
        temp_dict["station id"] = result.station
        temp_dict["name"] = result.name
        json_results.append(temp_dict)
    # close session
    # session.close()
    return jsonify(json_results)


if __name__ == '__main__':
    app.run(debug=True)
