from flask import Flask, render_template, request, session, redirect, url_for, flash
from dbconnect import connection
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from tweets import tweethub
from functools import wraps
from news import news
from india import nse_quote
from america import get_quote


app = Flask(__name__)
#tweets = tweethub()

# home page 
@app.route('/')
def homepage():
	description, title, desc_url, image_url = news()
	return render_template("news.html", news = zip(description, title, desc_url, image_url ))

# dashboard
@app.route('/dashboard/')
def dashboard():
	return render_template("dashboard.html")


@app.route('/india/')
def india():
	nsedata = nse_quote('infy')
	return render_template("india.html", nse = nsedata)

@app.route('/america/')
def america():
	
	ticker = 'AAPL'
	yahoo, quote, index, open_price, code = get_quote(ticker)
	return render_template("america.html", yahoo = yahoo, quote = quote, index = index, open_price = open_price, code = code)



# error handler
@app.errorhandler(404)
def notfound(e):
	return render_template("404.html")

# login page
@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

        	query = "SELECT * FROM users WHERE username = %s"
        	data = c.execute(query, (thwart(request.form['username']),))

        	if int(data) == 0:
        		error = "Invalid login credentials, please try again"

        	else:
        		data = c.fetchone()[2]
        		if sha256_crypt.verify(request.form['password'], data):
        			session['logged_in'] = True
        			session['username'] = request.form['username']

        			flash("you are now logged in")
        			return redirect(url_for('dashboard'))
        		
        		else:
        			error = "Invalid login credentials, please try again"       
            
		gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        flash(e)
        #error = "Invalid credentials, try again."
        return render_template("login.html", error = error)  

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			#flash ("you are already logged in")
			return f(*args, **kwargs)
		else:
			#flash ("you need to login to logout")
			return redirect(url_for('login_page'))
	return wrap


@app.route('/logout/')
@login_required
def logout():
	session.clear()
	gc.collect()
	return redirect(url_for('homepage'))




class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email Address', [validators.Length(min=6, max=35)])
	password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
# for registering the user
@app.route('/register/', methods = ['GET', 'POST'])
def register_page():
	try:
		form = RegistrationForm(request.form)
		if request.method == 'POST' and form.validate():
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt(str(form.password.data))

			c, conn = connection()
			query = "SELECT * FROM users WHERE username = %s"
			#x = c.execute("SELECT * FROM users WHERE username = ?" (thwart(username)))
			x = c.execute(query, (thwart(username),))
			#x = c.fetchone()
			if int(x) > 0:
				#flash ("that username already taken, please take another")
				return render_template("register.html", form =form, error = "Username is already taken")
			else:
				query2 = "INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)"
				#c.execute("INSERT INTO users (username, password, email, tracking) VALUES ({0}, {1}, {2}, {3})" .format(thwart(username), thwart(password), thwart(email), thwart('/home/')))
				c.execute(query2, (thwart(username), thwart(password), thwart(email), thwart('/home/')))
				conn.commit()
				#flash("Thanks for registering")
				c.close()
				conn.close()
				gc.collect()

				session['logged_in'] = True
				session['username'] = username
				return redirect(url_for('dashboard'))


		return render_template("register.html", form = form)
	except Exception as e:
		return render_template("register.html", error = e, form = form)



if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.run(debug = True)

    