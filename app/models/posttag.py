from app import db

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

