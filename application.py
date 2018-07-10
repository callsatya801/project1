import os

from flask import Flask, session, render_template, request, redirect, url_for, abort
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

#loginUser=None

#Validate Login/Pwd against Users Table
def valid_login(pUsername,pPassword):
    print("Inside valid_login method :")
    #session['loginUser']=pUsername
    #return True
    # Make sure valid user exists
    if db.execute("SELECT 'x' FROM users WHERE username = :uname and password = :pwd", {"uname": pUsername, "pwd":pPassword}).rowcount == 0:
        session.pop('loginUser', None)
        return False
    else:
        session['loginUser']=pUsername
        return True

#Validate existing user for Registration
def existing_user(pUsername,pPassword):
    print(f"Inside existing_user method :{pUsername}")

    if db.execute("SELECT 'x' FROM users WHERE username = :uname", {"uname": pUsername}).rowcount == 0:
           # Create User
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": pUsername, "password": pPassword})
        db.commit()
        return False
    else:
        return True


@app.route('/')
def index():
   print('before -- redirect')
   return redirect(url_for('login'))
   #return render_template('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    print("registration page")
    #return "registration page"
    message = None
    if request.method == 'POST':
        userName=request.form.get("inputUsername")
        pWord = request.form.get("inputPassword")
        print(f"request.form['inputUsername'] = {userName}, request.form['inputPassword']={pWord}" )

        if existing_user(userName,pWord):
            message = 'User already Exists - Please use different UserName. Existing User? Pleae Login.'
        else:
            print("Successful user creation - redirect to login page with success message")
            message = 'User Registration- Successful. Please login.'

    return render_template('register.html', message=message)



@app.route('/login',methods=['GET', 'POST'])
def login():
    #print(f"inside Login - method {request.method} - with loginUser:{session['loginUser']}")
    message = None
    if request.method == 'POST':
        userName=request.form.get("inputUsername")
        pWord = request.form.get("inputPassword")
        print(f"request.form['inputUsername'] = {userName}, request.form['inputPassword']={pWord}" )

        if valid_login(userName,pWord):
            print("Redirecting to Search")
            return redirect(url_for('search'))
            #return render_template('search.html')
        else:
            message = 'Invalid username/password - New User? Please Register.'
            return render_template('login.html', message=message)

    if request.method == 'GET' and  session.get('loginUser',None) is not None :
        #print(f"Before redirecting to Search Page - loginUser {session['loginUser']}")
        print(f"Before redirecting to Search Page - loginUser")
        return redirect(url_for('search'))
    else:
        #print(f"Before redirecting to Login Page - loginUser {session['loginUser']}")
        print(f"Before redirecting to Login Page - loginUser")
        return render_template('login.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('loginUser', None)
   return redirect(url_for('login'))

@app.route("/search",  methods=["GET", "POST"])
def search():
    # Validate UserLogged-in before able to search
    #print(f"User is Logged-in with User:{session['loginUser']}")
    print(f"User is Logged-in with User:{session.get('loginUser',None)}")
    if session.get('loginUser',None) is None:
           print("User not Logged-in. Redirecting to Login-page")
           return redirect(url_for('login'))

    # Get the Search String - and query the locatation DB in zipcode, city, state columns.
    searchStr=""
    locations=None
    if request.method == "POST":
        searchStr = request.form.get("srchStr")
        locations = db.execute("SELECT zipcode, city, state, population, latitude, longitude, location_id, (select count(*) from location_checkin lc, users u where u.user_id = lc.user_id and u.username=:pUsername and l.location_id = lc.location_id) checkin_count FROM location l where upper(zipcode||city||state) like '%'||upper(:x)||'%' order by city",{"pUsername": session.get('loginUser',None), "x": searchStr}).fetchall()
    return render_template("search.html", locations=locations)


@app.route("/location/<int:location_id>", methods=["GET", "POST"])
def location(location_id):
    # Validate UserLogged-in before able to get details
    print(f"User is Logged-in with User:{session.get('loginUser',None)}")
    if session.get('loginUser',None) is None:
           print("User not Logged-in. Redirecting to Login-page")
           return redirect(url_for('login'))

    """Lists details about a single location."""
    # Make sure location exists.
    loc = db.execute("SELECT zipcode, city, state, population, latitude, longitude, location_id FROM location WHERE location_id = :id", {"id": location_id}).fetchone()
    if loc is None:
        return render_template("error.html", message="No such Location.")

    # Get the location specific Weather Details from darksky API
    queryUrl = f"https://api.darksky.net/forecast/c5ec3ef072177608a06f858bc9544f05/{loc.latitude},{loc.longitude}"
    query = requests.get(queryUrl).json()
    current = query["currently"]

    # Get the check-in comments on this Location
    c_comments = db.execute("SELECT lc.comments, lc.checkin_time, u.username from location_checkin lc, users u where u.user_id = lc.user_id and  lc.location_id = :loc_id",{"loc_id": location_id).fetchall()

    # Is current User Checked-in
    curr_checkin = db.execute("SELECT 'x' from location_checkin lc, users u where u.user_id = lc.user_id and u.username=:pUsername and l.location_id = :loc_id",{"pUsername": session.get('loginUser',None), "loc_id": location_id}).fetchall()

    return render_template("location.html", location=loc, weather=current, c_comments=c_comments, is_current_checkin=curr_checkin )

#API Access: If users make a GET request to your website’s /api/<zip> route,
# where <zip> is a ZIP code, your website should return a JSON response containing (at a minimum)
# the name of the location, its state, latitude, longitude, ZIP code, population, and the number of user check-ins to that location.
@app.route("/api/<zipcode>")
def api(zipcode):
    """Get the Location details in JSON for given ZipCode."""

    # Make sure location exists.
    loc = db.execute("SELECT zipcode, city, state, population, latitude, longitude, location_id, (select count(*) from location_checkin lc where l.location_id = lc.location_id) checkin_count FROM location l WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()
    if loc is None:
        #return render_template("error.html", message="No such Location.")
        abort(404)

    # return all rows as a JSON array of objects
    #items = [dict(zip([key[0] for key in cursor.description], row)) for row in loc]
    locDict={
        'place_name': loc.city,
        'state': loc.state,
        'latitude': float(loc.latitude),
        'longitude': float(loc.longitude),
        'zip': loc.zipcode,
        'population': loc.population,
        'check_ins': loc.checkin_count
    }

    #locJson = json.dumps(locDict, indent = 2)
    return json.dumps(locDict, indent = 2)
    #return render_template("api.html", locJson=ppr, zipCode=zipcode)
