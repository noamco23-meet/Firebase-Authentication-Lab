from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import re


firebaseConfig = {
  "apiKey": "AIzaSyDGU7bZuWan1X850GTtFOXiksAfPQ6CBvs",
  "authDomain": "authentication-lab-b4c0c.firebaseapp.com",
  "projectId": "authentication-lab-b4c0c",
  "storageBucket": "authentication-lab-b4c0c.appspot.com",
  "messagingSenderId": "649855230347",
  "appId": "1:649855230347:web:5ed570815c258f6541cf8e",
  "measurementId": "G-QHK52F2Z76",
  "databaseURL": "https://authentication-lab-b4c0c-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed."
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "password":password}
            db.child("Users").child(login_session['user']['localId'].set(user))
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed."
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet = {"title": request.form['title'], "text": request.form['text'], "uid":login_session['user']['localId']}
        db.child("Tweets").push(tweet) 
        return redirect(url_for('all_tweets'))    
    else:
        return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/all_tweets')
def all_tweets():
    print(db.child("Tweets").get().val())
    return render_template("tweets.html", tweets = db.child("Tweets").get().val())

if __name__ == '__main__':
    app.run(debug=True)