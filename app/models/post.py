from app import db, app
from app.users import models



def searchPost(query=None, min_val=None, max_val=None, offset=None):
	app.logger.debug("entering searchPost")
	
	sql = "SELECT p.* "
	
	if query:
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
		
		if min_val:
			sql += "AND p.price > "+str(min_val)+" "
		if max_val:
			sql += "AND p.price < "+str(max_val)+" "

		sql += "GROUP BY p.id "
		sql += "ORDER BY p.update_date DESC "
		sql += "LIMIT 10 "
		if offset:
			sql += "OFFSET "+str(offset)

	else:
		sql += "FROM posts p "

		if min_val and not max_val:
			sql += "WHERE p.price > "+str(min_val) + " "
		elif max_val and not min_val:
			app.logger.debug("max and not min")
			sql += "WHERE p.price < "+str(max_val) + " "
			sql += "AND p.price > "+"0.0 "
		elif max_val and min_val:
			sql += "WHERE p.price < "+str(max_val) + " "
			sql += "AND p.price > "+str(min_val) + " "
		
		sql += "ORDER BY p.update_date DESC "
		sql += "LIMIT 10 "
		if offset:
			sql += "OFFSET "+str(offset)

	app.logger.debug(sql)
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
		price = row[11]
		post_date = row[12]
		update_date = row[13]

		post = models.Post(link, userid, groupid, fbid, price=price, photoid=photoid, album=album, thumbnail=thumbnail, body=body, likes=likes, category=category, post_date=post_date, update_date=update_date)
		post.id = id;
		posts.append(post)
	return posts

