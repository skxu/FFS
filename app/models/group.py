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

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

	def __repr__(self):
		return 'Group Name: %r\n' % (self.name)


def createGroup(fbid, name):
	group = Group(fbid, name)
	db.session.add(group)
	db.session.commit()
	return group

def getGroupFromFbid(fbid):
	group = Group.query.filter_by(fbid=fbid).first()
	if group:
		return group
	else:
		return None

'''
@graph - facebook-sdk graph object
@fbid - unique facebook ID number for the group
'''
def getGroupName(graph, fbid):
	group_data = graph.get_object(fbid)
	return group_data['name']