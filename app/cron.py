from app import db, app
from app.users import models
import facebook


print("hello from cron.py")

FB_API_VERSION = app.config['FB_API_VERSION']
FB_APP_ID = app.config['FB_APP_ID']
FB_APP_SECRET = app.config['FB_APP_SECRET']
FB_APP_NAME = app.config['FB_APP_NAME']

#this isn't really the right way to do things
ACCESS_TOKEN = app.config['ACCESS_TOKEN']

#temp
GROUP_ID = app.config['GROUP_ID']
print("GROUP_ID:", GROUP_ID)

#utilities
def getPostURL(id):
	url = "https://www.facebook.com/groups/"+GROUP_ID+"/permalink/"+id
	return url

#returns models.User
def getUserFromFbid(fbid):
	user = models.User.query.filter_by(fbid=fbid).first()
	if user:
		return user
	#no user with fbid, let's make one!
	else:
		user = models.User(fbid=fbid)
		db.session.add(user)
		db.session.commit()
		return user

#returns models.Post
def getPostFromFbid(fbid):
	post = models.Post.query.filter_by(fbid=fbid).first()
	if post:
		return post
	else:
		return None

def extendAccessToken():
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)
	graph.extend_access_token(FB_APP_ID,FB_APP_SECRET)


#important stuff
def getPosts():
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)

	group = graph.get_object(GROUP_ID)
	posts = graph.get_connections(GROUP_ID, "feed")
	
	for post in posts['data']:
		fb_postid = post['id']
		#see if the post already exists in our database
		post_obj = getPostFromFbid(fb_postid)
		if post_obj != None:
			print("post exists!", post_obj)
			#update the post if needed
		else:
			fb_userid = post['from']['id']
			userid = getUserFromFbid(fb_userid).id
			body = post['message']
			link = getPostURL(fb_postid)
			post_date = post['created_time']
			post = models.Post(link, userid, fb_postid, body=body, post_date=post_date)
			print("NEW POST!!!", post)
			db.session.add(post)
			db.session.commit()
			



getPosts() 