from app import db
from app.users import constants as USER

UNKNOWN_PRICE = float(-1)
UNKNOWN_TYPE = 0
SELL_TYPE = 1
BUY_TYPE = 2

class User(db.Model):

	__tablename__ = 'users_user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	fbid = db.Column(db.Integer, unique=True)
	name = db.Column(db.String(20))
	role = db.Column(db.SmallInteger, default=USER.USER)
	status = db.Column(db.SmallInteger, default=USER.INACTIVE)

	def __init__(self, name=None, username=None, email=None, password=None, fbid=None, status=None):
		self.username = username
		self.email = email
		self.password = password
		self.fbid = fbid
		self.name = name
		self.status = status

	def getStatus(self):
		return USER.STATUS[self.status]


	def getRole(self):
		return USER.ROLE[self.role]


	def __repr__(self):
		return '<User %r>' % (self.username)


#Class modeling the Free and For Sale groups in facebook
class Group(db.Model):
	__tablename__ = 'groups'
	id = db.Column(db.Integer, primary_key=True)
	fbid = db.Column(db.Integer, unique=True)
	name = db.Column(db.String(80))

	def __init__(self, fbid, name):
		self.name = name
		self.fbid = fbid

	def __repr__(self):
		return 'Group Name: %r\n' % (self.name)


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


	def __repr__(self):
		return '<Link: %r>\nBody:\n%r\n' % (self.link, self.body)


class Photo(db.Model):
	__tablename__ = "photos"
	id = db.Column(db.Integer, primary_key=True)
	fbid = db.Column(db.Integer, unique=True)
	source = db.Column(db.String(120))
	thumbnail = db.Column(db.String(120))
	body = db.Column(db.Text, nullable=True)

	def __init__(self, fbid, source, thumbnail, body=None):
		self.fbid = fbid
		self.source = source
		self.thumbnail = thumbnail
		self.body = body

	def __repr__(self):
		return "Source url:%r\n" % self.source


class Tag(db.Model):
	__tablename__ = "tags"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)


	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Tag %r>' % self.name


class Comment(db.Model):
	__tablename__ = "comments"
	id = db.Column(db.Integer, primary_key=True)
	fbid = db.Column(db.Integer, unique=True)
	postid = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
	body = db.Column(db.Text)
	userid = db.Column(db.Integer, db.ForeignKey("users_user.id"), nullable=False)
	create_date = db.Column(db.DateTime)
	update_date = db.Column(db.DateTime)

	def __init__(self, postid, fbid, userid, body=None, create_date=None, update_date=None):
		self.postid = postid
		self.fbid = fbid
		self.body = body
		self.userid = userid
		self.create_date = create_date
		self.update_date = update_date

	def __repr__(self):
		return "Comment: %r\n" % self.body

class PostTag(db.Model):
	__tablename__ = "posts_tags"
	id = db.Column(db.Integer, primary_key=True)
	postid = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
	tagid = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)

	def __init__(self, postid, tagid):
		self.postid = postid
		self.tagid = tagid

	def __repr__(self):
		return "Post ID: %r\nTag ID: %r\n" % (self.postid, self.tagid)


