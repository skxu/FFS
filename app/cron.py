from app import db, app
from app.users import models
from app.models import comment, group, photo, post, posttag, tag, user

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

debug = True
nuke = False
app.logger.debug("hello from cron.py")

FB_API_VERSION = app.config['FB_API_VERSION']
FB_APP_ID = app.config['FB_APP_ID']
FB_APP_SECRET = app.config['FB_APP_SECRET']
FB_APP_NAME = app.config['FB_APP_NAME']

#this isn't really the right way to do things
ACCESS_TOKEN = app.config['ACCESS_TOKEN']

#temp, eventually use ALLLL the groups
GROUP_ID = app.config['GROUP_ID']
app.logger.debug("GROUP_ID:" + str(GROUP_ID))

#utilities





def extendAccessToken():
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)
	graph.extend_access_token(FB_APP_ID,FB_APP_SECRET)


#important stuff that actually belongs in cron.py
def getPosts(group_id):
	graph = facebook.GraphAPI(ACCESS_TOKEN, FB_API_VERSION)

	group_obj = group.getGroupFromFbid(group_id)
	if not group_obj:
		name = group.getGroupName(graph, group_id)
		#obsolete
		#group_obj = createGroup(group_id, name)
		group_obj = group.Group(group_id, name)
		group_obj.save()

	posts_data = graph.get_connections(group_id, "feed", limit=100)
	processPosts(graph, group_obj, posts_data)
	
	#let's go through the old posts since we don't have that data yet!
	counter = 0
	while counter < 2:
		next_url = posts_data.get('paging').get('next')
		posts_data = graph.direct_request(next_url)
		processPosts(graph, group_obj, posts_data)
		counter+=1
		


def processPosts(graph, group_obj, posts_data):
	for post_data in posts_data.get('data'):
		#app.logger.debug(post)
		fb_postid = post_data.get('id')
		#see if the post already exists in our database
		post_obj = post.getPostFromFbid(fb_postid)
		if post_obj != None:
			app.logger.debug("post exists")
			#update the post if needed
			update_date = dateparser.parse(post_data.get('updated_time'))
			if update_date.replace(tzinfo=None) > post_obj.update_date.replace(tzinfo=None):
				#we need to update!
				post_obj.body = post_data.get('message')

				#TODO: refilter tags & stuff
				post_obj.update_date = update_date.replace(tzinfo=None)
				db.session.commit()
				
				comments_data = post_data.get('comments')
				processComments(post_obj, comments_data)

		#post does not exist in our database, make a new one		
		else:
			#assuming all posts have 'from'
			fb_userid = post_data.get('from').get('id')
			fb_name = post_data.get('from').get('name')
			
			#attempt to get user object, otherwise make one
			user_obj = user.getUserFromFbid(fb_userid)
			if not user_obj:
				#user_obj = user.createUser(fb_userid, name=fb_name)
				user_obj = user.User(fbid=fb_userid, name=fb_name)
				user_obj.save()

			body = post_data.get('message')
			
			#default price unknown
			price = post.UNKNOWN_PRICE
			
			#try to find price through regex matching
			if body:
				result = r.search(body)
				if result:
					price = float(result.group(1))
			

			comments_data = post_data.get('comments')
			link = post.getPostURL(fb_postid)

			album_link = None
			photo_obj = None
			thumbnail = None
			album_id = post_data.get('object_id')
			if album_id:
				#attempt to get photo object, otherwise make one
				photo_obj = photo.getPhotoFromFbid(album_id)
				album_link = photo.getAlbumURL(album_id)
				if not photo_obj:
					photo_info = photo.getPhotoInfo(graph, album_id)
					source = photo_info[0]
					thumbnail = photo_info[1]
					body = photo_info[2]
					#photo_obj = photo.createPhoto(album_id, source, thumbnail, body)
					photo_obj = photo.Photo(album_id, source, thumbnail, body)
					photo_obj.save()
			photoid = None if not photo_obj else photo_obj.id	
			post_date = dateparser.parse(post_data.get('created_time')).replace(tzinfo=None)
			#post_obj = post.createPost(link, user.id, group.id, fb_postid, price=price, photoid=photoid, album=album_link, thumbnail=thumbnail, body=body, post_date=post_date, update_date=post_date)
			post_obj = post.Post(link, user_obj.id, group_obj.id, fb_postid, price=price, photoid=photoid, album=album_link, thumbnail=thumbnail, body=body, post_date=post_date, update_date=post_date)
			post_obj.save()

			if debug:
				app.logger.debug("NEW POST!")
			
			stopwordcount = 0
			if body:
				for word in body.split(' '):
					word = word.lower()

					#strip out punctuation
					word = word.translate(punctuation)
					if word in stopwords:
						stopwordcount+=1
					else:
						tag_obj = tag.getTagFromName(word)
						if not tag_obj:
							#tag_obj = createTag(word)
							tag_obj = tag.Tag(word)
							tag_obj.save()
						#post_tag = posttag.createPostTag(post.id, tag.id)
						post_tag = posttag.PostTag(post_obj.id, tag_obj.id)
						post_tag.save()

			
			processComments(post_obj, comments_data)

def processComments(post_obj, comments_data):
	if comments_data == None:
		return
	for comment_data in comments_data.get('data'):
		fb_userid = comment_data.get('from').get('id')
		fb_commentid = comment_data.get('id')
		comment_obj = comment.getCommentFromFbid(fb_commentid)
		if comment_obj:
			continue
		fb_name = comment_data.get('from').get('name')
		user_obj = user.getUserFromFbid(fb_userid)
		if not user_obj:
			#user = createUser(fb_userid, name=fb_name)
			user_obj = user.User(fbid=fb_userid, name=fb_name)
			user_obj.save()
		body = comment_data.get('message')
		create_date = dateparser.parse(comment_data.get('created_time'))
		#comment_obj = createComment(post.id, fb_commentid, user.id, body=body, create_date=create_date)
		comment_obj = comment.Comment(post_obj.id, fb_commentid, user_obj.id, body=body, create_date=create_date)
		comment_obj.save()
			
if nuke:
	db.drop_all()
	db.create_all()

def updatePostsJob():
	getPosts(GROUP_ID)

scheduler = BackgroundScheduler()
scheduler.add_job(updatePostsJob, 'interval', seconds=30)
scheduler.start()


