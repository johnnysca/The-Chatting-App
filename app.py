from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Client import Client

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

client = [] # testing
# C1 = Client()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    global client # testing

    if request.method == 'POST': # if user submits a login check if it exists
        username = request.form.get('username')
        password = request.form.get('password')
        users = Users.query.filter_by(username=username).first() # get all the usernames that are in DB that match with entered username
        if users and users.password == password: # if username is found then check if the password is exact
            flash('Login successful!')
            session['username'] = username
            client.append(Client(session['username'])) # testing


            return redirect(url_for('chat'))
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

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        global client
        if client:
            if request.method == "POST":
                print(session['username'], ':', request.form.get('message'))
                print("client2 ", client)
                client.send_message(request.form.get('message'))
                return render_template('chat.html')
            return render_template('chat.html')
        else:
            return render_template('chat.html')

app.secret_key = 'temporary keyu'

if __name__ == '__main__':
    app.run(debug=True)