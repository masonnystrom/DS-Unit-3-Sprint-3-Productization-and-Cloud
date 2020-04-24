from flask import Flask
from myapi import api_client
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, redirect

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# database class
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Time (' + str(self.datetime) + ',' + str(self.value) + ')'

# Routes for dashboard 
@APP.route('/')
def root():
    """Base view."""
    smog_level = Record.query.filter(Record.value>=10).all()
    # return str(smog_level)
    return render_template("/index.html", smog_level=smog_level)


# api that pulls the data
@APP.route("/data")
def api_pull():
    api = api_client()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']
    data = []
    for result in results:
        date = result['date']['utc']
        value = result['value']
        data.append((date, value))
    return data

# route that refreshes the data into the database
@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = api_pull()
    for date, value in data:
        record = Record(datetime=date, value=value)
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'

# api pulls the cityes and number of measurements 
@APP.route('/cities')
def get_cities():
    """ Gets a list of tuples and the count of measurements for the city 
    """
    api = api_client()
    status, resp = api.cities()
    results = resp['results']
    
    data = [] # empty list to append data
    for result in results:
        city = result["city"]
        count = result["count"]
        data.append((city, count))
    return(str(data))