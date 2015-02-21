from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os, time, ConfigParser
import facebook



API_VERSION = 2.2
FB_APP_ID = ''
FB_APP_SECRET = ''
FB_APP_NAME = ''
ACCESS_TOKEN = 'CAAUuHZADBcskBAJB3S2EVIqwYSqk8zDFNVZB9jQX7ppEzFreWdZCuAK6zniTdIwk9cXLObuTjYRLYvg8ZCJv0sXBcNOzMoFkJSJp9n7ywksCakzyfH0psjnCo4h4V4mL8n4XZCdfZAcN2s8fvCZCTdRMXge1dR4de1B3hCziDTC4E2GZBZB0nBurXgVttpspRYMwfvLGLsBFbORWXw5I5QVTo'

#Set up your ID, SECRET, & NAME
#This section is hardcoded
Config = ConfigParser.ConfigParser()
Config.read("fb.cfg")
FB_APP_ID = Config.get('AppInfo','FB_APP_ID')
FB_APP_SECRET = Config.get('AppInfo', 'FB_APP_SECRET')
FB_APP_NAME = Config.get('AppInfo', 'FB_APP_NAME')



app = Flask("FFS")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tml/app.db'
db = SQLAlchemy(app)

api = restful.Api(app)


def refreshAppAccessToken():
	#This will get an app access token, which unfortunately won't work for FFS
	ACCESS_TOKEN = facebook.get_app_access_token(FB_APP_ID, FB_APP_SECRET)

def getTime():
	print("Time is: %s" % datetime.now())


def extendAccessToken():
	graph = facebook.GraphAPI(ACCESS_TOKEN, API_VERSION)
	graph.extend_access_token(FB_APP_ID,FB_APP_SECRET)

def getPosts():
	graph = facebook.GraphAPI(ACCESS_TOKEN, API_VERSION)
	
	group = graph.get_object("266259930135554")
	posts = graph.get_connections("266259930135554", "feed")
	print(posts)



class HelloWorld(restful.Resource):
	def get(self):
		return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

scheduler = BackgroundScheduler()
#scheduler.add_job(refreshAccessToken, 'interval', seconds=7200)
scheduler.start()

getPosts()


app.run(debug=True, use_reloader=False)