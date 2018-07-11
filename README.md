# Project 1

Web Programming with Python and JavaScript

Registration: Users should be able to register for your website, providing (at minimum) a username and password.
>> register.html: Users will be redirected to Login page if user is not logged-in and given option to navigate to Registration.
>> Used hashlib.sha1 to encrypt password. Use encription to compare the user input.

Login: Users, once registered, should be able to log in to your website with their username and password.
>>On successful login the user is redirected to search page - to search for weather forecast

Logout: Logged in users should be able to log out of the site.
>> Once user is logged-in, on Top Right of Search and Locations page Logged-in user name is displayed along with the option to click on log-out button.
>> User will not be logged-off is browser is closed. User have to click on "logout" button to logout.

Import: Provided for you in this project is a file called zips.csv, which is a file in CSV format of all ZIP codes in the United States that have a population of 15,000
>> Load process is implimented in "import.py". Added left padding zero's (0) if lenght of the zip codes provided in the file is < 5 digits.

Search: Once a user has logged in, they should be taken to a page where they can search for a location. Users should be able to type a ZIP code or the name of a city or town. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches at all. If the user typed in only partial information, your search page should find matches for those as well!
>>User will be able to search by entering partial string of state, city or zip code. Empty string is validated and appropriate warning message is shown on search page.

Location Page: When users click on a location from the results of the search page, they should be taken to a page for that location, with details about the location coming from your database: the name of the location, its ZIP code, its latitude and longitude, its population, and the number of check-ins and the written comments that users have left for the location on your website.
Dark Sky Weather Data: On your location page, you should also display information about the current weather, displaying minimally the time of the weather report, the textual weather summary (e.g. “Clear”), temperature, dew point, and humidity (as a percentage). You can display more information if you wish.
>> Location page displays - current Temperature and Time (Local Time of the location - returned by DarkSky api). All other attributes of json attributes on Current shown as additional details.
>> Added new element in Json for WeekDay based on the unixtime for Daily Forecast table. Daily forecast table shows Min and Max temperatures of the Day.

Check-In Submission: On the location page, users should be able to submit a “check-in”, consisting of a button that allows them to log a visit, as well as a text component where the user can provide comments about the location. Users should not be able to submit more than one check-in for the same location or edit a comment they have previously left. Users should only be able to submit a check-in if they are logged in.
>> User is provided an option to enter comments under the "check-in image" for check-in. Once user clicks on Check-in, comments and Check-in time is recorded for the at location per user.
>> Comments left by other users are displayed in Check-in Section fo the location page.

API Access: If users make a GET request to your website’s /api/<zip> route, where <zip> is a ZIP code, your website should return a JSON response containing (at a minimum) the name of the location, its state, latitude, longitude, ZIP code, population, and the number of user check-ins to that location. The resulting JSON should follow the format; the order of the keys is not important, so long as they are all present:
{
    "place_name": "Cambridge",
    "state": "MA",
    "latitude": 42.37,
    "longitude": -71.11,
    "zip": "02138",
    "population": 36314,
    "check_ins": 1
}
>> No login validation for the API access. Used jsonify to return json object.

If the requested ZIP code isn’t in your database, your website should return a 404 error.
>> used abort() function to return 404 error.

References:
>> Clouds/Check-in images are downladed from https://pixabay.com - available for free download once login.

Notes:
Added Houly/Daily Forecast