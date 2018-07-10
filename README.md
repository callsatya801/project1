# Project 1

Web Programming with Python and JavaScript

Registration: Users should be able to register for your website, providing (at minimum) a username and password.
>>

Login: Users, once registered, should be able to log in to your website with their username and password.
>>

Logout: Logged in users should be able to log out of the site.
>>

Import: Provided for you in this project is a file called zips.csv, which is a file in CSV format of all ZIP codes in the United States that have a population of 15,000 or more (there are 7375 such ZIP codes; apologies if your own hometown or ZIP code is not included as a result!) as well as some other information such as location names and short codes, latitude and longitude, and population. In a Python file called import.py separate from your web application, write a program that will take the information in this CSV and import it into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python import.py to import the locations into your database, and submit this program with the rest of your project code.
>>

Search: Once a user has logged in, they should be taken to a page where they can search for a location. Users should be able to type a ZIP code or the name of a city or town. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches at all. If the user typed in only partial information, your search page should find matches for those as well!
>>

Location Page: When users click on a location from the results of the search page, they should be taken to a page for that location, with details about the location coming from your database: the name of the location, its ZIP code, its latitude and longitude, its population, and the number of check-ins and the written comments that users have left for the location on your website.
>>

Check-In Submission: On the location page, users should be able to submit a “check-in”, consisting of a button that allows them to log a visit, as well as a text component where the user can provide comments about the location. Users should not be able to submit more than one check-in for the same location or edit a comment they have previously left. Users should only be able to submit a check-in if they are logged in.
>>

Dark Sky Weather Data: On your location page, you should also display information about the current weather, displaying minimally the time of the weather report, the textual weather summary (e.g. “Clear”), temperature, dew point, and humidity (as a percentage). You can display more information if you wish.
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
If the requested ZIP code isn’t in your database, your website should return a 404 error.
