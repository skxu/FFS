from app import db

class Tag(db.Model):
	__tablename__ = "tags"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)


	def __init__(self, name):
		self.name = name

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

	def __repr__(self):
		return '<Tag %r>' % self.name



def getTagFromName(name):
	tag = Tag.query.filter_by(name=name).first()
	if tag:
		return tag
	else:
		return None

def createTag(name):
	tag = Tag(name)
	db.session.add(tag)
	db.session.commit()
	return tag

