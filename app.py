from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from datetime import datetime

#Connect to database
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect Database to ORM Classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#Get Table References
Measurement = Base.classes.Measurement
Station = Base.classes.Station

session = Session(engine)


#Define Flask
app = Flask(__name__)

#create loading route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

#Create Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():

	#Define query
	precipitation = session.query(Measurement.DATE, Measurement.PRCP)\
		.filter(Measurement.ISODATE > '2016-08-22 00:00:00.000000').group_by(Measurement.ISODATE).\
		order_by(Measurement.ISODATE).all()

	#list
	ly_precipitation = []

	#create dict and then append to list
	for day in precipitation:
		prec_dict = {}
		prec_dict['Date'] = day.DATE
		prec_dict['PRCP'] = day.PRCP
		ly_precipitation.append(prec_dict)

	#jsonify
	return jsonify(ly_precipitation)

#Create Stations Route
@app.route("/api/v1.0/stations")
def stations():

	#define query
	stations = session.query(Station.STATION, Station.NAME).all()
	Measurements = session.query(Measurement.STATION).distinct(Measurement.STATION).all()

	#Create measurement list to check Stations query against
	Measurelist = []

	for row in Measurements:
		Measurelist.append(row.STATION)

	#Create station list composed of items from station
	Stationlist = []

	for row in stations:
		#check if the station is in the Distinct List. My way out of the lack of foreign keys.
		if row.STATION in Measurelist:
			station_dict = {}
			station_dict['station'] = row.STATION
			station_dict['name'] = row.NAME
			Stationlist.append(station_dict)

	#jsonify results
	return jsonify(Stationlist)

#Create TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():

	#define query
	tobs = session.query(Measurement.DATE, Measurement.TOBS, Measurement.STATION)\
	.filter(Measurement.ISODATE > '2016-08-22 00:00:00.000000').group_by(Measurement.ISODATE).\
	order_by(Measurement.ISODATE).all()

	#Create tobs list composed of TOBS data
	tobslist = []

	for row in tobs:
		tobs_dict = {}
		tobs_dict['Date'] = row.DATE
		tobs_dict['station'] = row.STATION
		tobs_dict['TOBS'] = row.TOBS
		tobslist.append(tobs_dict)

	#jsonify results
	return jsonify(tobslist)

#Create Temp List for Min, Avg, and Max Temperatures
#First Route - No End Specified
@app.route("/api/v1.0/<string:start>")
def startonly(start):

	#Convert to datetime object, if needed
	date = datetime.strptime(start, '%Y-%m-%d')

	#Get Minimum temperature
	minimum = session.query(func.min(Measurement.TOBS)).filter(Measurement.ISODATE > start).all()

	#Get Maximum temperature
	maximum = session.query(func.max(Measurement.TOBS)).filter(Measurement.ISODATE > start).all()

	#Get Average temperature
	average = session.query(func.avg(Measurement.TOBS)).filter(Measurement.ISODATE > start).all()

	#create dict
	tempdict = {'min': minimum, 'max': maximum, 'avg': average}

	# return jsonify(date)
	return jsonify(tempdict)

@app.route("/api/v1.0/<string:start>/<string:end>")
def startend(start,end):

	#Get Minimum
	minimum = session.query(func.min(Measurement.TOBS)).filter(Measurement.ISODATE > start).filter(Measurement.ISODATE > end).all()

	#Get Maximum
	maximum = session.query(func.max(Measurement.TOBS)).filter(Measurement.ISODATE > start).filter(Measurement.ISODATE > end).all()

	#Get Average Temperature
	average = session.query(func.avg(Measurement.TOBS)).filter(Measurement.ISODATE > start).filter(Measurement.ISODATE > end).all()

	#create dict
	tempdict = {'min': minimum, 'max': maximum, 'avg': average, 'start': start, 'end': end}

	#return jsonify
	return jsonify(tempdict)

if __name__ == '__main__':
    app.run(debug=True)