#All API Calls to NPS will be made here 
import requests
import os

#Base URL of the National Park Service for use with the API
base_url = "https://developer.nps.gov/api/v1/"

def url(path):
	return base_url+path

#Park Data
def getParks(state="", code="", keyword=""):
	return requests.get(url("parks?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Event Data
def getEvents(state, code, keyword):
	return requests.get(url("events?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Visitor Center Data
def getVisitorCenters(state, code, keyword):
	return requests.get(url("visitorcenters?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Alert Data
def getAlerts(state, code, keyword):
	return requests.get(url("alerts?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#News Data
def getNewsreleases(state, code, keyword):
	return requests.get(url("newsreleases?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#People Data
def getPeople(state, code, keyword):
	return requests.get(url("people?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Lesson Plan Data 
def getLessonplans(state, code, keyword):
	return requests.get(url("lessonplans?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Article Data
def getArticles(state, code, keyword):
	return requests.get(url("articles?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Campground Data
def getCampgrounds(state, code, keyword):
	return requests.get(url("campgrounds?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))

#Places Data 
def getPlaces(state, code, keyword):
	return requests.get(url("places?parkCode=%s&stateCode=%s&q=%s&api_key=%s") % 
		(code, state, keyword, os.environ.get('NPS_API_KEY')))


