from app import db
from app.users import models


def searchPost(query):
	sql  = "SELECT p.* "
	sql += "FROM tags t, posts p, posts_tags pt "
	sql += "WHERE pt.tagid = t.id "
	sql += "AND (t.name in ("
	for word in query.split(" "):
		if not word or word == '':
			continue
		sql+="'"+word+"', "
	sql  = sql[:-2]
	sql += ")) "
	sql += "AND p.id = pt.postid "
	sql += "GROUP BY p.id"
	print(sql)
	result = db.engine.execute(sql)
	posts = []
	for row in result:
		id = row[0]
		fbid = row[1]
		link = row[2]
		album = row[3]
		thumbnail = row[4]
		body = row[5]
		likes = row[6]
		category = row[7]
		userid = row[8]
		groupid = row[9]
		photoid = row[10]
		post_date = row[11]
		update_date = row[12]

		post = models.Post(link, userid, groupid, fbid, photoid=photoid, album=album, thumbnail=thumbnail, body=body, likes=likes, category=category, post_date=post_date, update_date=update_date)
		post.id = id;
		posts.append(post)
	return posts

