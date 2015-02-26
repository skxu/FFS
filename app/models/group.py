from app import db

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

