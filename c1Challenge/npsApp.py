from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import random
import os
from forms import ApiCallForm

from apiCalls import *

import parkCodes


app = Flask(__name__)

app.config['SECRET_KEY'] = "c69369a241a1a01734cc61a70f71579efbaedeb53e588e4e"

# ---------------------------------------------------------------------------


#Base URL of the National Park Service for use with the API
base_url = "https://developer.nps.gov/api/v1/"

#Home page
@app.route('/')
@app.route("/home", methods=["GET","POST"])
def home():
	form = ApiCallForm()
	todaysFeaturedPark = featuredPark()
	return render_template("home.html", title = "Kiosk Home", form = form, todaysFeaturedPark = todaysFeaturedPark)

#Home search results page
@app.route('/searchResults', methods=["GET","POST"])
def parkSearchResults():
	parks = (getParks(request.form['stateAbbreviation'],
		 request.form['parkCode'],
		 request.form['keyword'])).json()
	parksData = parks['data']	
	return render_template("homeResults.html", title = "Search Results", parksData = parksData)

#Individual Park Search Results Page (Main Info center of Web App)
@app.route('/individualPark/<string:data>', methods=["GET","POST"])
def individualParkResults(data):
	#API call to /parks
	individualPark = (getParks("",data,"")).json()

	#API call to/alerts
	individualAlerts = (getAlerts("",data,"")).json()
	individualAlerts = individualAlerts['data']

	#API call to /events
	individualEvents = (getEvents("",data,"")).json()
	individualEvents = individualEvents['data']

	#API call to /visitorcenters
	individualVisitorcenter = (getVisitorCenters("",data,"")).json()
	individualVisitorcenter = individualVisitorcenter['data']

	#API call to /newsreleases 
	individualNews = (getNewsreleases("",data,"")).json()
	individualNews = individualNews['data']

	#API call to /people
	individualPeople = (getPeople("",data,"")).json()
	individualPeople = individualPeople['data']

	#API call to /places
	individualPlaces = (getPlaces("",data,"")).json()
	individualPlaces = individualPlaces['data']

	#API call to /articles
	individualArticles = (getArticles("",data,"")).json()
	individualArticles = individualArticles['data'][0]

	#Gets the latest newsrelease
	if len(individualNews) > 0:
		individualNews = individualNews[0]

	individualParkData = individualPark['data']
	individualParkDataTest = individualParkData[0]

	#Get lat and long data for static google map image
	parkLatLong = individualParkDataTest['latLong']
	parkLat, parkLong = parkLatLong.split(",")

	#Format the string properly for static google map api 
	parkLat = parkLat[4:]
	parkLong = parkLong[6:]
	finalParkLatLong = parkLat + "," + parkLong

	#Make API call to Google Maps and store it in variable 
	googleStaticMapImg = "https://maps.googleapis.com/maps/api/staticmap?markers=%s&zoom=5&size=500x500&key=%s" % (finalParkLatLong, os.environ.get('GOOGLE_API_KEY'))

	#Pass all relevant data to individualpark.html page
	return render_template("individualParks.html", title = "Individual Park Results", 
		specificPark = individualParkDataTest, specificNews = individualNews,
		individualAlerts = individualAlerts, individualVisitorcenter = individualVisitorcenter,
		individualPeople = individualPeople, individualPlaces = individualPlaces,
		individualArticles = individualArticles, googleImage = googleStaticMapImg)

#Function generates a random featured park for home page
def featuredPark():
	#Generate a random number
	randomParkCode = random.randint(0,409)

	while True:
		#Make api call with a random park code from the list of parkcodes in parkCodes.py
		featuredPark = (getParks("",str(parkCodes.allParkCodes[randomParkCode]),"")).json()
		#Get the data portion of the API Call
		featuredPark = featuredPark['data']
		#Check to make sure there is actual data associated with the random park code
		if len(featuredPark) > 0:
			featuredPark = featuredPark[0]
			#Return the featured Park to /home
			return featuredPark

#Lesson Plan and People Page
@app.route('/lessonplans', methods = ["GET","POST"])
def lessonplans():
	form = ApiCallForm()
	return render_template("lessonplans.html", title = "Lesson Plans", form = form)

#Lesson Plan Search Results page
@app.route('/lessonplanSearchResults', methods = ["GET","POST"])
def lessonplansResults():

	#API call to /lessonplans
	allLessonplans = (getLessonplans(request.form['stateAbbreviation'],
		 request.form['parkCode'],
		 request.form['keyword'])).json()

	#API call to /people
	allPeople = (getPeople(request.form['stateAbbreviation'],
		 request.form['parkCode'],
		 request.form['keyword'])).json()

	#Retrieve data portion of the returned json 
	allLessonplans = allLessonplans['data']
	allPeople = allPeople['data']

	#Send relevant data to lessonplansResults.html
	return render_template("lessonplansResults.html", title = "Lessonplans Results", lessonplanData = allLessonplans,
		peopleData = allPeople)

#Events page
@app.route('/eventsAtParks/<string:data>', methods = ["GET","POST"])
def eventsAtParks(data):
	#API call to /events
	individualEvents = (getEvents("",data,"")).json()
	individualEvents = individualEvents['data']

	return render_template("eventsAtParks.html", title = "Events at Park", individualEvents = individualEvents)

#About page
@app.route('/about')
def about():
    return render_template("about.html", title = 'About')

#Places to Park Page
@app.route('/placesAtParks/<string:data>', methods = ["GET","POST"])
def placesAtParks(data):
	#API call to /places
	places = (getPlaces("",data,"")).json()
	places = places['data']

	park = (getParks("", data,"")).json()
	park = park['data'][0]['fullName']

	return render_template("placesAtParks.html", title = "Places at Park", places = places,
		park = park)

#Articles Page
@app.route("/articles", methods = ["GET", "POST"])
def articles():
	form = ApiCallForm()
	return render_template("articles.html", title = articles, form = form)

#Articles Search Results Page 
@app.route('/articlesSearchResults', methods = ["GET","POST"])
def articlesResults():

	#API call to /articles
	allArticles = (getArticles(request.form['stateAbbreviation'],
		 request.form['parkCode'],
		 request.form['keyword'])).json()

	#Retrieve data portion of the returned json 
	allArticles = allArticles['data']

	return render_template("articlesResults.html", title = "Articles Results", articlesData = allArticles)

#Campgrounds Page 
@app.route("/campgrounds", methods = ["GET", "POST"])
def campgrounds():
	form = ApiCallForm()
	return render_template("campgrounds.html", title = campgrounds, form = form)


#Campgrounds Search Results Page 
@app.route('/campgroundsSearchResults', methods = ["GET","POST"])
def campgroundsResults():

	#API call to /campgrounds
	allCampgrounds = (getCampgrounds(request.form['stateAbbreviation'],
		 request.form['parkCode'],
		 request.form['keyword'])).json()

	#Retrieve data portion of the returned json 
	allCampgrounds = allCampgrounds['data']


	return render_template("campgroundsResults.html", title = "Campground Results", campgroundsData = allCampgrounds)






