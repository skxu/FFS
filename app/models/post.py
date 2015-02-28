from app import db, app
from app.models.user import User
from app.models.comment import Comment
from app.models.photo import Photo

UNKNOWN_PRICE = float(-1)
UNKNOWN_TYPE = 0
SELL_TYPE = 1
BUY_TYPE = 2

def searchPost(query=None, min_val=None, max_val=None, offset=None):
	app.logger.debug("entering searchPost")
	
	sql = "SELECT p.* "
	
	if query:
		sql += "FROM tags t, posts p, posts_tags pt "
		sql += "WHERE pt.tagid = t.id "
		sql += "AND (t.name in ("
		for word in query.split(" "):
			if not word or word == '':
				continue
			sql+="'"+word+"', "
		sql  = sql[:-2]
		sql += ")) "
		sql += "AND p.id = pt.postid "
		
		if min_val:
			sql += "AND p.price > "+str(min_val)+" "
		if max_val:
			sql += "AND p.price < "+str(max_val)+" "

		sql += "GROUP BY p.id "
		sql += "ORDER BY p.update_date DESC "
		sql += "LIMIT 10 "
		if offset:
			sql += "OFFSET "+str(offset)

	else:
		sql += "FROM posts p "

		if min_val and not max_val:
			sql += "WHERE p.price > "+str(min_val) + " "
		elif max_val and not min_val:
			app.logger.debug("max and not min")
			sql += "WHERE p.price < "+str(max_val) + " "
			sql += "AND p.price > "+"0.0 "
		elif max_val and min_val:
			sql += "WHERE p.price < "+str(max_val) + " "
			sql += "AND p.price > "+str(min_val) + " "
		
		sql += "ORDER BY p.update_date DESC "
		sql += "LIMIT 10 "
		if offset:
			sql += "OFFSET "+str(offset)

	app.logger.debug(sql)
	result = db.engine.execute(sql)
	posts = []
	for row in result:
		id = row[0]
		fbid = row[1]
		link = row[2]
		album = row[3]
		thumbnail = row[4]
		body = row[5]
		likes = row[6]
		category = row[7]
		userid = row[8]
		groupid = row[9]
		photoid = row[10]
		price = row[11]
		post_date = row[12]
		update_date = row[13]

		post = Post(link, userid, groupid, fbid, price=price, photoid=photoid, album=album, thumbnail=thumbnail, body=body, likes=likes, category=category, post_date=post_date, update_date=update_date)
		post.id = id;
		posts.append(post)
	return posts



class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	fbid = db.Column(db.Integer, unique = True)
	link = db.Column(db.String(80))
	album = db.Column(db.String(80), nullable=True)
	thumbnail = db.Column(db.String(80), default="/static/img/thumb.png")
	body = db.Column(db.Text)
	likes = db.Column(db.Integer, default=0)
	category = db.Column(db.Integer, default=UNKNOWN_TYPE)
	userid = db.Column(db.Integer, db.ForeignKey("users_user.id"), nullable=False)
	groupid = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
	photoid = db.Column(db.Integer, db.ForeignKey("photos.id"), nullable=True)
	price = db.Column(db.Float, default=UNKNOWN_PRICE)
	post_date = db.Column(db.DateTime)
	update_date = db.Column(db.DateTime)


	def getUser(self):
		return User.query.filter_by(id=self.userid).first()

	def getComments(self):
		comments = Comment.query.filter_by(postid=self.id).order_by(Comment.create_date).all()
		return comments

	def getPhoto(self):
		if not self.photoid:
			return None
		
		photo = Photo.query.filter_by(id=self.photoid).first()
		return photo



	def __init__(self, link, userid, groupid, fbid, photoid=None, album=None, thumbnail=None, body=None, likes=0, category=None, price=None, post_date=None, update_date=None):
		self.link = link
		self.album = album
		self.thumbnail = thumbnail
		self.body = body
		self.likes = likes
		self.category = category
		self.userid = userid
		self.groupid = groupid
		self.fbid = fbid
		self.photoid = photoid
		self.price = price
		self.post_date = post_date
		self.update_date = update_date

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

	def __repr__(self):
		return '<Link: %r>\nBody:\n%r\n' % (self.link, self.body)



def createPost(link, userid, groupid, fbid, price=None, photoid=None, album=None, thumbnail=None, body=None, likes=0, post_date=None, update_date=None):
	post = Post(link, userid, groupid, fbid, price=price, photoid=photoid, album=album, thumbnail=thumbnail, body=body, likes=likes, post_date=post_date, update_date=update_date)
	db.session.add(post)
	db.session.commit()
	return post

#returns Post
def getPostFromFbid(fbid):
	post = Post.query.filter_by(fbid=fbid).first()
	if post:
		return post
	else:
		return None

def getPostURL(id):
	id_list = id.split("_")
	group_id = id_list[0]
	post_id = id_list[1]
	url = "https://www.facebook.com/groups/"+group_id+"/permalink/"+post_id
	return url
