from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    return 'Hello World!'

# /api/v1.0/precipitation

@app.route('/api/v1.0/precipitation')
def precipitation():
    # start session
    session = Session(engine)
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    query_results = session.query(Measurement.date, Measurement.prcp).all()
    # convert it to json first
    json_results = []
    for result in query_results:
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
    query_results = session.query(Measurement.tobs).all()
    # convert it to json first
    json_results = []
    for result in query_results:
        json_results.append(result.tobs)
    # close session
    session.close()
    return jsonify(json_results)
    
    


if __name__ == '__main__':
    app.run()
