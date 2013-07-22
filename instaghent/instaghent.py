
from google.appengine.api import memcache

from instagram import client, subscriptions
from google.appengine.ext import db
import geo.geomodel
import simplejson as json

from google.appengine.ext.db import stats


CONFIG = {
	'client_id': 'a5a67115f0fc45d6b97d318ac915aa91',
	'client_secret': '76458a657e8c4317a32ebb9b8b224219',
	'redirect_uri': 'http://localhost:8002/oauth_callback'
}

api = client.InstagramAPI(**CONFIG)

class Photo(db.Model):
	author = db.StringProperty()
	ID = db.StringProperty()
	profile_picture = db.LinkProperty()

	filters = db.StringProperty()
	time = db.DateTimeProperty()
	tags = db.StringListProperty()
	ghents = db.IntegerProperty()
	likes = db.IntegerProperty()
	caption = db.TextProperty()
	location = db.GeoPtProperty()

	comments = db.IntegerProperty()

	link = db.LinkProperty()
	standard = db.LinkProperty()
	thumb = db.LinkProperty()
	low = db.LinkProperty()

def create_new_photo(photo):
	tags = []
	for tag in photo.tags:
		tags.append(tag.name)
	key_name = "photo/%s" % photo.id
	query = Photo.get_or_insert(
			key_name = key_name,
			ID = photo.id,
			author = photo.user.username,
			profile_picture = photo.user.profile_picture,
			filters = photo.filter,
			time = photo.created_time,
			ghents = 0,
			tags = tags,
			likes = len(photo.likes),
			comments = len(photo.comments),
			link = photo.link,
			low = photo.images["low_resolution"].url,
			thumb = photo.images["thumbnail"].url,
			standard = photo.images["standard_resolution"].url,
		)
	changes = False
	if hasattr(photo.caption, "text"):
		if (query.caption == None):
			query.caption = photo.caption.text
			changes = True
	if hasattr(photo, "location"):
		if (query.location == None):
			if (photo.location.point != None):
				query.location = db.GeoPt(photo.location.point.latitude, photo.location.point.longitude)
				changes = True
	if (changes == True): query.put()

	return query


def gql_json_parser(query_obj):
    result = []
    for entry in query_obj:
        result.append(dict([(p, unicode(getattr(entry, p))) for p in entry.properties()]))
    return result

def single_gql_json_parser(entry):
    result = dict([(p, unicode(getattr(entry, p))) for p in entry.properties()])
    return result
  
def clear_cache(): 
	filters = ["time","likes","comments","ghents", "taggf13"]
	for n in range(0, 200, 10):
		memcache.delete_multi([filter+str(n) for filter in filters])
	return memcache.delete_multi(filters)


def collectFiles():
	photos, next = api.tag_recent_media(count=30, tag_name="ghent")
	for photo in photos:
		create_new_photo(photo)
	clear_cache();

def collectFilesInsta():
	photos, next = api.tag_recent_media(count=30, tag_name="instaghent")
	for photo in photos:
		create_new_photo(photo)
	clear_cache();

def collectOne():
	photos, next = api.tag_recent_media(count=1, tag_name="gf13")
	for photo in photos:
		create_new_photo(photo)
	filters = ["taggf13"]
	for n in range(0, 200, 10):
		memcache.delete_multi([filter+str(n) for filter in filters])
	memcache.delete_multi(filters)
	return photos

def collectFilesFieste():
	photos, next = api.tag_recent_media(count=30, tag_name="gf13")
	for photo in photos:
		create_new_photo(photo)
	photos, next = api.tag_recent_media(count=30, tag_name="gentsefeesten")
	for photo in photos:
		create_new_photo(photo)
	clear_cache();

def InitFieste():
	amo = 0
	photos, next = api.tag_recent_media(count=30, tag_name="gf13")
	for photo in photos:
		create_new_photo(photo)
	amo += len(photos)
	page = photos[len(photos)-1].id
	for x in range(1, 20):
		photos, next = api.tag_recent_media(count=30, max_id=page, tag_name="gf13")
		for photo in photos:
			create_new_photo(photo)
		page = photos[len(photos)-1].id
		amo += len(photos)
	clear_cache();
	return amo

def collectFilesLong():
	photos, next = api.tag_recent_media(count=30, tag_name="ghent")
	for photo in photos:
		create_new_photo(photo)
	clear_cache();


def fetchImages(sortingMethod = "time"):
	key_cache = sortingMethod
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		q = Photo.gql("ORDER BY %s DESC" % sortingMethod)
		data = json.dumps(gql_json_parser(q.fetch(limit=10)))
		memcache.add(key_cache, data, 3600)
		return json.loads(data)

def fetchFieste(sortingMethod = "tag", tagid = "gf13"):
	key_cache = sortingMethod + tagid
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		q = Photo.all()
		q.filter("tags IN", [tagid])
		q.order("-time")
		data = json.dumps(gql_json_parser(q.fetch(limit=10)))
		memcache.add(key_cache, data, 3600)
		return json.loads(data)

def fetchFiestePage(sortingMethod = "tag", tagid = "gf13", more = 10):
	key_cache = sortingMethod+tagid+more
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		q = Photo.all()
		q.filter("tags IN", [tagid])
		q.order("-time")
		data = json.dumps(gql_json_parser(q.fetch(limit=10, offset=int(more))))
		memcache.add(key_cache, data, 3600)
		return json.loads(data)


def fetchPage(sortingMethod = "time", more = 10):
	key_cache = sortingMethod+more
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		q = Photo.gql("ORDER BY %s DESC" % sortingMethod)
		data = json.dumps(gql_json_parser(q.fetch(limit=10, offset=int(more))))
		memcache.add(key_cache, data, 3600)
		return json.loads(data)

def fetchAll(sortingMethod = "likes"):
	key_cache = sortingMethod+"all"
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		data = json.dumps(gql_json_parser(Photo.all().order(sortingMethod)))
		memcache.add(key_cache, data, 3600)
		return json.loads(data)

def fetchLocation():
	key_cache = "location"
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		data = json.dumps(gql_json_parser(Photo.all().filter("location !=", None)))
		memcache.add(key_cache, data, 9600)
		return json.loads(data)

def fetchbyAuthor(authorname):
	key_cache = "author"+authorname
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		data = json.dumps(gql_json_parser(Photo.gql("WHERE author = '%s'" % authorname).fetch(limit=10)))
		memcache.add(key_cache, data, 1800)
		return json.loads(data)

def fetchImage(photoid):
	key_cache = "photo"+photoid
	data = memcache.get(key_cache)
	if data is not None:
		return json.loads(data);
	else:
		data = json.dumps(single_gql_json_parser(Photo.gql("WHERE ID = '%s'" % photoid).get()))
		memcache.add(key_cache, data, 9600)
		return json.loads(data)


def upGhentImage(photoid):
	q = Photo.gql("WHERE ID = '%s'" % photoid).get()
	q.ghents = q.ghents + 1
	q.put()
	return q.ghents

def downGhentImage(photoid):
	q = Photo.gql("WHERE ID = '%s'" % photoid).get()
	q.ghents = q.ghents - 1
	q.put()
	return q.ghents

def deleteFiles(sortingMethod = "time"):
	q = Photo.gql("WHERE ghents < 0")
	x = q.fetch(limit=20)
	ids = []
	for item in x:
		if hasattr(item, "id"):
			memcache.delete("photo"+item.id)
		item.delete()
	clear_cache();
	return len(x)
