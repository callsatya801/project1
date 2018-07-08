import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import datetime
import json

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

loginUser="satya"

@app.route("/")
def index():
    # Show Search page if User already logged-in
    # Check the login-session
    if loginUser is not None or loginUser!="":
        return render_template("login.html")
    else:
        # Re-direct to Login/Register Page
        #return "Project 1: TODO"
        return render_template("search.html")

@app.route("/search",  methods=["GET", "POST"])
def search():
    # Get the Search String - and query the locatation DB in zipcode, city, state columns.
    searchStr=""
    if request.method == "POST":
        searchStr = request.form.get("srchStr")
    locations = db.execute("SELECT zipcode, city, state, population, latitude, longitude, location_id FROM location where upper(zipcode||city||state) like '%'||upper(:x)||'%' order by city",{"x": searchStr}).fetchall()
    return render_template("search.html", locations=locations)


@app.route("/location/<int:location_id>")
def location(location_id):
    """Lists details about a single location."""

    # Make sure location exists.
    loc = db.execute("SELECT zipcode, city, state, population, latitude, longitude, location_id FROM location WHERE location_id = :id", {"id": location_id}).fetchone()
    if loc is None:
        return render_template("error.html", message="No such Location.")

    # Get the location specific Weather Details from darksky API
    queryUrl = f"https://api.darksky.net/forecast/c5ec3ef072177608a06f858bc9544f05/{loc.latitude},{loc.longitude}"
    query = requests.get(queryUrl).json()

    return render_template("location.html", location=loc, weather=query)

#API Access: If users make a GET request to your website’s /api/<zip> route,
# where <zip> is a ZIP code, your website should return a JSON response containing (at a minimum)
# the name of the location, its state, latitude, longitude, ZIP code, population, and the number of user check-ins to that location.
@app.route("/api/<zipcode>")
def api(zipcode):
    """Get the Location details in JSON for given ZipCode."""

    # Make sure location exists.
    loc = db.execute("SELECT zipcode, city, state, population, latitude, longitude, location_id FROM location WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()
    if loc is None:
        return render_template("error.html", message="No such Location.")

    # return all rows as a JSON array of objects
    #items = [dict(zip([key[0] for key in cursor.description], row)) for row in loc]
    locDict={
    "place_name": loc.city,
    "state": loc.state,
    "latitude": float(loc.latitude),
    "longitude": float(loc.longitude),
    "zip": loc.zipcode,
    "population": loc.population,
    "check_ins": 1
    }

    locJson = json.dumps(locDict, indent = 2)
    return locJson
    #return render_template("api.html", locJson=ppr, zipCode=zipcode)
