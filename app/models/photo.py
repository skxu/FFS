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

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

	def __repr__(self):
		return "Source url:%r\n" % self.source


def createPhoto(fbid, source, thumbnail, body):
	photo = Photo(fbid,source,thumbnail, body=body)
	db.session.add(photo)
	db.session.commit()
	return photo

def getPhotoFromFbid(fbid):
	photo = Photo.query.filter_by(fbid=fbid).first()
	if photo:
		return photo
	else:
		return None

def getAlbumURL(fbid):
	url = "https://www.facebook.com/photo.php?fbid="+fbid
	return url

def getPhotoInfo(graph, fbid):
	photo_obj = graph.get_object(fbid)
	#app.logger.debug("THIS IS A PHOTO: "+str(photo))
	thumbnail = photo_obj.get('picture')
	source = photo_obj.get('source')
	body = photo_obj.get('name')
	return (source, thumbnail, body)