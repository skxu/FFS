from app import db

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

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

	def __repr__(self):
		return "Comment: %r\n" % self.body


#not using update_date for now
def createComment(postid, fbid, userid, body, create_date):
	comment = Comment(postid, fbid, userid, body=body, create_date=create_date)
	db.session.add(comment)
	db.session.commit()
	return comment


def getCommentFromFbid(fbid):
	comment = Comment.query.filter_by(fbid=fbid).first()
	if comment:
		return comment
	else:
		return None