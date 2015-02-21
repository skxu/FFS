from app import db, app
from app.users import models
import facebook
import dateutil.parser as dateparser


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
	id_list = id.split("_")
	group_id = id_list[0]
	post_id = id_list[1]
	url = "https://www.facebook.com/groups/"+group_id+"/permalink/"+post_id
	return url

#returns models.User
def getUserFromFbid(fbid):
	user = models.User.query.filter_by(fbid=fbid).first()
	if user:
		return user
	else:
		return None

def createUser(fbid, name=None):
	user = models.User(fbid=fbid, name=name)
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

def getGroupFromFbid(fbid):
	group = models.Group.query.filter_by(fbid=fbid).first()
	if group:
		return group
	else:
		return None

def getGroupName(graph, fbid):
	group = graph.get_object(fbid)
	return group['name']

def createGroup(fbid, name):
	group = models.Group(fbid, name)
	db.session.add(group)
	db.session.commit()
	return group

def extendAccessToken():
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)
	graph.extend_access_token(FB_APP_ID,FB_APP_SECRET)


#important stuff
def getPosts(group_id):
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)

	group = getGroupFromFbid(group_id)
	if not group:
		name = getGroupName(graph, group_id)
		group = createGroup(group_id, name)

	posts = graph.get_connections(group_id, "feed")
	
	for post in posts['data']:
		fb_postid = post['id']
		#see if the post already exists in our database
		post_obj = getPostFromFbid(fb_postid)
		if post_obj != None:
			print("post exists!", post_obj)
			#update the post if needed
		else:
			fb_userid = post['from']['id']
			fb_name = post['from']['name']
			user = getUserFromFbid(fb_userid)
			
			#create new user if not in database
			if not user:
				user = createUser(fb_userid, name=fb_name)

			body = post['message']
			link = getPostURL(fb_postid)
			print(dateparser.parse(post['created_time']))
			post_date = dateparser.parse(post['created_time'])
			post = models.Post(link, user.id, group.id, fb_postid, body=body, post_date=post_date)
			print("NEW POST!!!", post)
			db.session.add(post)
			db.session.commit()
			



getPosts(GROUP_ID) 