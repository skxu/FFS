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
#these need to be put into respective models eventually
def getPostURL(id):
	id_list = id.split("_")
	group_id = id_list[0]
	post_id = id_list[1]
	url = "https://www.facebook.com/groups/"+group_id+"/permalink/"+post_id
	return url

def getAlbumURL(fbid):
	url = "https://www.facebook.com/photo.php?fbid="+fbid
	return url

def getPhotoURLs(graph, fbid):
	photo = graph.get_object(fbid)
	thumbnail = photo.get('picture')
	source = photo.get('source')
	return (source, thumbnail)

def getPhotoFromFbid(fbid):
	photo = models.Photo.query.filter_by(fbid=fbid).first()
	if photo:
		return photo
	else:
		return None

def createPhoto(fbid, source, thumbnail):
	photo = models.Photo(fbid,source,thumbnail)
	db.session.add(photo)
	db.session.commit()
	return photo

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
	
	for post in posts.get('data'):
		fb_postid = post.get('id')
		#see if the post already exists in our database
		post_obj = getPostFromFbid(fb_postid)
		if post_obj != None:
			print("post exists!", post_obj)
			#update the post if needed
		else:
			#assuming all posts have 'from'
			fb_userid = post.get('from').get('id')
			fb_name = post.get('from').get('name')
			
				
			user = getUserFromFbid(fb_userid)
			
			#create new user if not in database
			if not user:
				user = createUser(fb_userid, name=fb_name)

			body = post.get('message')
			link = getPostURL(fb_postid)
			album_link = None
			photo = None
			album_id = post.get('object_id')
			if album_id:
				photo = getPhotoFromFbid(album_id)
				album_link = getAlbumURL(album_id)
				if not photo:
					photo_urls = getPhotoURLs(graph, album_id)
					source = photo_urls[0]
					thumbnail = photo_urls[1]
					photo = createPhoto(album_id,source,thumbnail)
			photoid = None if not photo else photo.id	
			post_date = dateparser.parse(post.get('created_time'))
			post = models.Post(link, user.id, group.id, fb_postid, photoid=photoid, album=album_link, body=body, post_date=post_date)
			print("NEW POST!!!", post)
			db.session.add(post)
			db.session.commit()
			

db.drop_all()
db.create_all()

getPosts(GROUP_ID) 