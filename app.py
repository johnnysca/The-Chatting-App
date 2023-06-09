from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Client import Client
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0011223344@localhost/logins'
app.config['SECRET_KEY'] = 'A temporary secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
Session(app)
socketio = SocketIO(app, manage_session=False)

# defaultroom = 'room1' # this is so everyone joins the same room if not everyone will be in their own rooms

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
        username = request.form.get('username')
        password = request.form.get('password')
        users = Users.query.filter_by(username=username).first() # get all the usernames that are in DB that match with entered username
        if users and users.password == password: # if username is found then check if the password is exact
            flash('Login successful!')
            session['username'] = username
            print("sessions ", session['username'])
            return redirect(url_for('room'))
        else:
            flash('Username or password are incorrect')
            return render_template('login.html')
    else:
        if 'username' in session: # user is still signed in, no need to re-sign in
            return redirect('/room')
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
        defaultroom = request.form['room']
        session['room'] = defaultroom
        if request.method == "POST":
            return render_template('chat.html')
        return render_template('chat.html')


@app.route('/room', methods=['GET', 'POST'])
def room():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == "POST":

            return render_template('room.html')
        return render_template('room.html')


@socketio.on('join', namespace='/chat') # for when you join the chatroom
def join(message):
    defaultroom = session.get('room')
    join_room(defaultroom)
    emit('status', {'msg': session['username'] + ' has joined the chat'}, room=defaultroom)


@socketio.on('text', namespace='/chat') # for when you send a message
def text(message):
    defaultroom = session.get('room')
    emit('message', {'msg': session['username'] + ': ' + message['msg']}, room=defaultroom)


@socketio.on('left', namespace='/chat') # for when you leave a chat server
def left(message):
    username = session.get('username')
    defaultroom = session.get('room')
    print(username, defaultroom)
    leave_room(defaultroom)
    # session.clear()
    emit('status', {'msg': username + ' has left the chat'}, room=defaultroom)


if __name__ == '__main__':
    socketio.run(app, debug=True)