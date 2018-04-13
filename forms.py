from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired("Please enter your first name")])
	last_name = StringField('Last name', validators=[DataRequired("Please enter your last name")])
	email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter your email address correctly")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password"), Length(min=6, message="Password must be at least 6 characters long")])
	submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter a correct email address")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password")])
	submit = SubmitField("Sign in")

class AddBookForm(FlaskForm):
	isbn = IntegerField('ISBN Number', validators=[DataRequired("Please enter the isbn of the book")])
	bookName = StringField('Book Name', validators=[DataRequired("Please enter the name of the book")])
	authorName = StringField('Author Name', validators=[DataRequired("Please enter the name of the Author")])
	coverImg = StringField('CoverImageName')
	submit = SubmitField('Add book')