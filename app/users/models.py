from app import db
from app.users import constants as USER

class User(db.Model):

	__tablename__ = 'users_user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	role = db.Column(db.SmallInteger, default=USER.USER)
	status = db.Column(db.SmallInteger, default=USER.ACTIVE)

	def __init__(self, username=None, email=None, password=None):
		self.username = username
		self.email = email
		self.password = password

	def getStatus(self):
		return USER.STATUS[self.status]


	def getRole(self):
		return USER.ROLE[self.role]

	def __repr__(self):
		return '<User %r>' % (self.username)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	body = db.Column(db.Text)
	post_date = db.Column(db.DateTime)


	def __init__(self, title=None, body=None, post_date=None):
		self.title = title
		self.body = body
		self.post_date = post_date

	def __repr__(self):
		return '<Title: %r>\nBody:\n%r\n' % (self.title, self.body)







class Tag(db.Model):
	__tablename__ = "tags"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)



	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Tag %r>' % self.name