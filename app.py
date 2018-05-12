from flask import Flask, render_template, request, session, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_caching import Cache
from models import User, Books
from forms import SignupForm, LoginForm, SearchBookForm
from books import queryBooks

db = MongoEngine()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
		'db': 'LibraryApp',
		'username': 'ashans',
		'password': 'powermate24'
}

db.init_app(app)

app.secret_key = "development-key"

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

########################################################################################################

# Home screen: First thing a user sees. Before and after login.
@app.route("/")
def home():
	if 'email' in session:
		return render_template("home.html", signin=True, username=session['user_name'])
	else:
		return render_template("home.html", signin=False)


# Sign up screen: A sign up form for signing up purposes. 		
@app.route("/signup", methods=['GET', 'POST'])
def signup():

	if 'email' in session:
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			#TODO: find a way to hash password during initialization
			newuser.set_password(form.password.data)
			newuser.save()

			session['email']=newuser.email
			return redirect(url_for('home'))

	elif request.method == "GET":
		return render_template('signup.html', form=form)


# Log in screen: A log in form with email and password. 
@app.route("/login", methods=["GET", "POST"])
def login():
	if 'email' in session:
		return redirect(url_for('home'))

	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.objects(email=email).first()

			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				session['user_name'] = user.firstname
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))

	elif request.method == "GET":
		return render_template('login.html', form=form)


# Log out route: Logs out by deleting email in the session dictionary. 
#	Redirects to home. 
@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('home'))


# Search screen: Contains a single search 
@app.route("/searchbooks", methods=["GET"])
#@app.route("/searchbooks/<search_param>", methods=["GET", "POST"]) 
#@cache.cached(timeout=60)
def searchBooks():
	if 'email' not in session:
		return redirect(url_for('login'))

	searchbookForm = SearchBookForm()

	return render_template('searchbooks.html',  signin=True, form=searchbookForm, search=False)
		
@app.route("/searchbooks/<search_param>/<page_num>", methods=["GET", "POST"]) 
def showBooks(search_param, page_num):
	if 'email' not in session:
		return redirect(url_for('login'))

	if request.method == "POST":
		bookList = queryBooks(search_param)
		print(bookList)

		return bookList

##########################################################################################################################

#@app.errorhandler()

##########################################################################################################################

if __name__ == "__main__":
	app.run(debug=True)