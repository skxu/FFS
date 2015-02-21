from app import db, app
from app.users import models
from words import stopwords, punctuation
import string
import facebook
import dateutil.parser as dateparser

debug = True
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

def getTagFromName(name):
	tag = models.Tag.query.filter_by(name=name).first()
	if tag:
		return tag
	else:
		return None

def createTag(name):
	tag = models.Tag(name)
	db.session.add(tag)
	db.session.commit()
	return tag

def createPostTag(postid, tagid):
	post_tag = models.PostTag(postid, tagid)
	db.session.add(post_tag)
	db.session.commit()
	return post_tag

def createPost(link, userid, groupid, fbid, photoid=None, album=None, body=None, likes=0, post_date=None):
	post = models.Post(link, userid, groupid, fbid, photoid=photoid, album=album, body=body, likes=likes, post_date=post_date)
	db.session.add(post)
	db.session.commit()
	return post

def extendAccessToken():
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)
	graph.extend_access_token(FB_APP_ID,FB_APP_SECRET)


#important stuff that actually belongs in cron.py
def getPosts(group_id):
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)

	group = getGroupFromFbid(group_id)
	if not group:
		name = getGroupName(graph, group_id)
		group = createGroup(group_id, name)

	posts = graph.get_connections(group_id, "feed", limit=100)
	print(posts.get('paging'))
	processPosts(graph, group, posts)
	
	#let's go through the old posts since we don't have that data yet!
	if debug:
		counter = 0
		while counter < 5:
			next_url = posts.get('paging').get('next')
			posts = graph.direct_request(next_url)
			processPosts(graph, group, posts)
			counter+=1
		
		

def processPosts(graph, group, posts):
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
			
			#attempt to get user object, otherwise make one
			user = getUserFromFbid(fb_userid)
			if not user:
				user = createUser(fb_userid, name=fb_name)

			body = post.get('message')
			link = getPostURL(fb_postid)
			album_link = None
			photo = None
			album_id = post.get('object_id')
			
			if album_id:
				#attempt to get photo object, otherwise make one
				photo = getPhotoFromFbid(album_id)
				album_link = getAlbumURL(album_id)
				if not photo:
					photo_urls = getPhotoURLs(graph, album_id)
					source = photo_urls[0]
					thumbnail = photo_urls[1]
					photo = createPhoto(album_id,source,thumbnail)
			photoid = None if not photo else photo.id	
			post_date = dateparser.parse(post.get('created_time'))
			post = createPost(link, user.id, group.id, fb_postid, photoid=photoid, album=album_link, body=body, post_date=post_date)
			if debug:
				print("NEW POST!!!", post)
			stopwordcount = 0
			if body:
				for word in body.split(' '):
					word = word.lower()

					#strip out punctuation
					word = word.translate(punctuation)
					if word in stopwords:
						stopwordcount+=1
					else:
						tag = getTagFromName(word)
						if not tag:
							tag = createTag(word)
						post_tag = createPostTag(post.id, tag.id)
			if debug:
				print ("stopwordcount", stopwordcount)

			
			

db.drop_all()
db.create_all()

getPosts(GROUP_ID) 