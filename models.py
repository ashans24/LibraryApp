from mongoengine import *
from werkzeug import generate_password_hash, check_password_hash

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

	# GoodReads Book ID
	goodreads_book_id = IntField(required=False)

	# Book's Name
	bookName = StringField(required=True)

	# GoodReads Author ID
	goodreads_author_id = IntField(required=False)

	# Author's Name
	authorName = StringField(required=True)

	# Publication date
	publish_year = IntField(required=True, null=True)

	# Number of reviews
	numOfReviews = IntField(required=True)

	# Average ratings
	avgRatings = DecimalField(required=True, min_value=0, max_value=5, precision=1)

	# Total number of ratings
	numOfRatings = IntField(required=True)

	# Book cover image
	#coverImg = StringField(required=True, null=True)

	# Genre of the book
	#genre = ListField()