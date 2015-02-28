from app import db

class PostTag(db.Model):
	__tablename__ = "posts_tags"
	id = db.Column(db.Integer, primary_key=True)
	postid = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
	tagid = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)

	def __init__(self, postid, tagid):
		self.postid = postid
		self.tagid = tagid

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

	def __repr__(self):
		return "Post ID: %r\nTag ID: %r\n" % (self.postid, self.tagid)


def createPostTag(postid, tagid):
	post_tag = PostTag(postid, tagid)
	db.session.add(post_tag)
	db.session.commit()
	return post_tag

