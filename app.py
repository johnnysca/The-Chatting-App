from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0011223344@localhost/logins'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST': # if user submits a login check if it exists
        session['username'] = request.form.get('username') # session will keep track of who is logged in
        session['password'] = request.form.get('password')
        print(session['username'])
        print(session['password'])
        users = Users.query.filter_by(username=session['username']).first() # get all the usernames that are in DB that match with entered username
        if users and users.password == session['password']: # if username is found then check if the password is exact
            flash('Login successful!')
            return render_template('chat.html')
        else:
            flash('Username or password are incorrect')
            return render_template('login.html')
    else:
        if 'username' in session: # user is still signed in, no need to re-sign in
            return redirect('/chat')
        return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST': # if user submits a login credential to signup then store it in DB
        username = request.form['username']
        password = request.form['password']
        new_user = Users(username=username, password=password) # Create Users object to store the credentials

        try:
            db.session.add(new_user) # send it to the DB
            db.session.commit()
            return redirect('/login')
        except Exception as e: # the entered credentials already exist so tell them and redirect to error.html
            flash("User already exists. Try another username")
            return render_template('signup.html')
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    flash('You have been logged out.')
    session.pop('username', None) # log out the user
    return render_template('logout.html')

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html')
    else:
        return redirect(url_for('login'))

app.secret_key = 'temporary keyu'

if __name__ == '__main__':
    app.run(debug=True)