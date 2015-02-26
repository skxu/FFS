from app import db


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