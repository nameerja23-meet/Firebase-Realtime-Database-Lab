from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config ={
	"apiKey": 
	"AIzaSyAsubGHZPFlrj0b0C9pDXSDjYmuHNbkkVw",
	"authDomain": "meet-lab1.firebaseapp.com",
	"projectId": "meet-lab1",
	"storageBucket": "meet-lab1.appspot.com",
	"messagingSenderId": "1068937932839",
	"appId": "1:1068937932839:web:ef0897418bc364394a9e02",
	"measurementId": "G-324B2TXS7T",
	"databaseURL":"https://meet-lab1-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		username = request.form['username']
		bio = request.form['bio']
		user = {'name': name, 'username': username, 'bio': bio}
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			db.child('Users').child(login_session['user']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
			return render_template("signup.html", error = 'Authentication failed', username = username)
	return render_template("signup.html")


@app.route('/signout')
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		title = request.form['title']
		text = request.form['description']
		tweet = {'title': title, 'text': text, 'uid':login_session['user']['localId']}
		db.child('Tweets').child(login_session['user']['localId']).push(tweet)
	return render_template("add_tweet.html")


@app.route('/all_tweets')
def all_tweets():
	tweets = db.child('Tweets').child(login_session['user']['localId']).get().val().values()
	return render_template("all_tweets.html", tweets = tweets)

if __name__ == '__main__':
	app.run(debug=True)