from app import db
from app.users import constants as USER

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

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self


	def __repr__(self):
		return '<User %r>' % (self.username)


#returns User
def getUserFromFbid(fbid):
	user = User.query.filter_by(fbid=fbid).first()
	if user:
		return user
	else:
		return None

def createUser(fbid, name=None):
	user = User(fbid=fbid, name=name)
	db.session.add(user)
	db.session.commit()
	return user
