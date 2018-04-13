from mongoengine import *
from werkzeug import generate_password_hash, check_password_hash

import json

try:
	from urllib.request import urlopen
	from urllib import parse
except ImportError:
	from urllib2 import urlopen, urlparse as parse


# Model for Users that use the application
class User(Document):
	#first name of user
	firstname = StringField(max_length=50)

	#last name of user
	lastname = StringField(max_length=50)

	#email of user
	email = EmailField(required=True, max_length=50, unique=True)

	#password of user
	password = StringField(required=True, min_length=6) 

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

# Model for Books
class Books(Document):
	# ISBN
	isbn = LongField(unique=True, required=True, null=False)

	# Book's Name
	bookName = StringField(required=True)

	# Author's Name
	authorName = StringField(required=True)

	# Book cover image
	coverImg = StringField(required=True, null=True)

	# Genre of the book
	#genre = ListField()

	def query(self, searchParam):
		key = 'TPC3VnClaHo1iI1xGPI5A'

		query_url = 'https://www.goodreads.com/search/index.xml?key={0}&q="{1}"'.format(key, searchParam)
		print(query_url)
		g = urlopen(query_url)
		results = g.read()
		g.close()

		print(results)

		# data = json.loads(results)

		# places = []
		# for place in data['query']['geosearch']:
		# 	name = place['title']
		# 	meters = place['dist']
		# 	lat = place['lat']
		# 	lng = place['lon']

		# 	wiki_url = self.wiki_path(name)
		# 	walking_time = self.meters_to_walking_time(meters)

		# 	d = { 
		# 		'name': name, 
		# 		'url': wiki_url,
		# 		'time': walking_time,
		# 		'lat': lat,
		# 		'lng': lng
		# 	}

		# 	places.append(d)

		return None