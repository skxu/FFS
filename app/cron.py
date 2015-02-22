from app import db, app
from app.users import models
from words import stopwords, punctuation
from apscheduler.schedulers.background import BackgroundScheduler
import string
import re
import facebook
import logging
import dateutil.parser as dateparser

logging.basicConfig()

#find the price in the post
r = re.compile("[\$](\d+(?:\.\d{1,2})?)")

PRICE_UKNOWN = float(-1)
debug = True
nuke = True
print("hello from cron.py")

FB_API_VERSION = app.config['FB_API_VERSION']
FB_APP_ID = app.config['FB_APP_ID']
FB_APP_SECRET = app.config['FB_APP_SECRET']
FB_APP_NAME = app.config['FB_APP_NAME']

#this isn't really the right way to do things
ACCESS_TOKEN = app.config['ACCESS_TOKEN']

#temp, eventually use ALLLL the groups
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

def getPhotoInfo(graph, fbid):
	photo = graph.get_object(fbid)
	print("THIS IS A PHOTO", photo)
	thumbnail = photo.get('picture')
	source = photo.get('source')
	body = photo.get('name')
	return (source, thumbnail, body)

def getPhotoFromFbid(fbid):
	photo = models.Photo.query.filter_by(fbid=fbid).first()
	if photo:
		return photo
	else:
		return None

def createPhoto(fbid, source, thumbnail, body):
	photo = models.Photo(fbid,source,thumbnail, body=body)
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

def createPost(link, userid, groupid, fbid, price=None, photoid=None, album=None, thumbnail=None, body=None, likes=0, post_date=None, update_date=None):
	post = models.Post(link, userid, groupid, fbid, price=price, photoid=photoid, album=album, thumbnail=thumbnail, body=body, likes=likes, post_date=post_date, update_date=update_date)
	db.session.add(post)
	db.session.commit()
	return post

def getCommentFromFbid(fbid):
	comment = models.Comment.query.filter_by(fbid=fbid).first()
	if comment:
		return comment
	else:
		return None

#not using update_date for now
def createComment(postid, fbid, userid, body, create_date):
	comment = models.Comment(postid, fbid, userid, body=body, create_date=create_date)
	db.session.add(comment)
	db.session.commit()
	return comment

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
	processPosts(graph, group, posts)
	
	#let's go through the old posts since we don't have that data yet!
	if debug:
		counter = 0
		while counter < 50:
			next_url = posts.get('paging').get('next')
			posts = graph.direct_request(next_url)
			processPosts(graph, group, posts)
			counter+=1
		


def processPosts(graph, group, posts):
	for post in posts.get('data'):
		print(post)
		fb_postid = post.get('id')
		#see if the post already exists in our database
		post_obj = getPostFromFbid(fb_postid)
		if post_obj != None:
			print("post exists!", post_obj)
			#update the post if needed
			update_date = dateparser.parse(post.get('updated_time'))
			if update_date.replace(tzinfo=None) > post_obj.update_date.replace(tzinfo=None):
				#we need to update!
				print("updating post",update_date.replace(tzinfo=None), post_obj.update_date.replace(tzinfo=None))
				post_obj.body = post.get('message')
				
				if post_obj.body == None:
					print("AHHH", post)
			

				#TODO: refilter tags & stuff
				post_obj.update_date = update_date.replace(tzinfo=None)
				db.session.commit()
				
				comments = post.get('comments')
				processComments(post_obj, comments)

		#post does not exist in our database, make a new one		
		else:
			#assuming all posts have 'from'
			fb_userid = post.get('from').get('id')
			fb_name = post.get('from').get('name')
			
			#attempt to get user object, otherwise make one
			user = getUserFromFbid(fb_userid)
			if not user:
				user = createUser(fb_userid, name=fb_name)

			body = post.get('message')
			price = PRICE_UKNOWN
			if body:
				result = r.search(body)
				if result:
					price = float(result.group(1))
			
			comments = post.get('comments')
			link = getPostURL(fb_postid)

			album_link = None
			photo = None
			thumbnail = None
			album_id = post.get('object_id')
			if album_id:
				#attempt to get photo object, otherwise make one
				photo = getPhotoFromFbid(album_id)
				album_link = getAlbumURL(album_id)
				if not photo:
					photo_info = getPhotoInfo(graph, album_id)
					source = photo_info[0]
					thumbnail = photo_info[1]
					body = photo_info[2]
					photo = createPhoto(album_id, source, thumbnail, body)
			photoid = None if not photo else photo.id	
			post_date = dateparser.parse(post.get('created_time')).replace(tzinfo=None)
			post = createPost(link, user.id, group.id, fb_postid, price=price, photoid=photoid, album=album_link, thumbnail=thumbnail, body=body, post_date=post_date, update_date=post_date)
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

			
			processComments(post, comments)

def processComments(post, comments):
	if comments == None:
		return
	for comment in comments.get('data'):
		fb_userid = comment.get('from').get('id')
		fb_commentid = comment.get('id')
		comment_obj = getCommentFromFbid(fb_commentid)
		if comment_obj:
			continue
		fb_name = comment.get('from').get('name')
		user = getUserFromFbid(fb_userid)
		if not user:
			user = createUser(fb_userid, name=fb_name)
		body = comment.get('message')
		create_date = dateparser.parse(comment.get('created_time'))
		comment = createComment(post.id, fb_commentid, user.id, body=body, create_date=create_date)
			
if nuke:
	db.drop_all()
	db.create_all()

def updatePostsJob():
	getPosts(GROUP_ID)

scheduler = BackgroundScheduler()
scheduler.add_job(updatePostsJob, 'interval', seconds=120)
scheduler.start()


