from flask import Flask, render_template, request, session, redirect, url_for
from flask_mongoengine import MongoEngine
from models import User
from forms import SignupForm, LoginForm

db = MongoEngine()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
		'db': 'LibraryApp',
		'username': 'ashans',
		'password': 'powermate24'
}

db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def home():
	if 'email' in session:
		return render_template("home.html", signin=True)
	else:
		return render_template("home.html", signin=False)


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
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))

	elif request.method == "GET":
		return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(debug=True)