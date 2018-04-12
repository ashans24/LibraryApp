from mongoengine import *
from werkzeug import generate_password_hash, check_password_hash

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