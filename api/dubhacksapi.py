from flask_restful import Resource, Api
from flask import Blueprint, session, redirect, url_for, render_template, request, Flask
from flask_socketio import emit, join_room, leave_room, SocketIO
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from flask_cors import CORS
import random
import MySQLdb
from time import sleep
from threading import Lock


main = Blueprint('main', __name__)
socketio = SocketIO()
app = Flask(__name__)
CORS(app)
api = Api(app)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

db = MySQLdb.connect(host="localhost", user="root",
                     passwd="root", db="DubHacks2017")
cur = db.cursor()

LFP = set()

thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    global LFP
    while session.get('room') in LFP:
        sleep(1)
        if len(LFP) >= 2:
            pair = random.sample(LFP, 2)
            LFP = LFP - set(pair)
            x = random.randint(1, 10**7)
            emit('joinroom', {'room': x}, room=pair[0])
            emit('joinroom', {'room': x}, room=pair[1])
            break


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Chatroom')


@socketio.on('lookingforgroup', namespace='/chat')
def lookingforgroup(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    global LFP
    global thread
    session['username'] = message['username']
    session['room'] = message['username']
    print("in looking for group", message['username'])
    room = session.get('room')
    join_room(room)
    LFP.add(room)
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('actuallyjoinroom', namespace='/chat')
def actuallyjoinroom(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print("in actuallyjoinroom")
    room = message['room']
    leave_room(session.get('username'))
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': message['msg'], 'username': message['username']}, room=room)


# @socketio.on('left', namespace='/chat')
# def left(message):
#     """Sent by clients when they leave a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     leave_room(room)
#     emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


# @main.route('/', methods=['GET', 'POST'])
# def index():
#     """Login form to enter a room."""
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         session['room'] = form.room.data
#         return redirect(url_for('.chat'))
#     elif request.method == 'GET':
#         form.name.data = session.get('name', '')
#         form.room.data = session.get('room', '')
#     return render_template('index.html', form=form)


# @main.route('/chat')
# def chat():
#     """Chat room. The user's name and room must be stored in
#     the session."""
#     name = session.get('name', '')
#     room = session.get('room', '')
#     if name == '' or room == '':
#         return redirect(url_for('.index'))
#     return render_template('chat.html', name=name, room=room)


class randomSEwebsite(Resource):
    def get(self):
        websites = {
            "Arash": "http://arashrai.com",
            "Stephen": "https://melinysh.me",
            "James": "http://jameshageman.com",
            "Matt": "http://mattdsouza.com",
            "Holly": "http://hollyoegema.com",
            "George": "http://georgeutsin.com/",
            "Spencer": "http://spencerdobrik.com/",
            "Liam": "http://liamca.xyz/",
            "Ryan": "http://www.ryan-martin.ca/",
            "Denton": "http://dentonliu.com/",
            "Stanley": "http://stanhuan.com/",
            "Prilik": "http://prilik.com/",
            "Kevin": "http://kpeng.ca/",
            "Tyler": "http://tnychka.me",
        }
        omit = request.args.get('omit')  # e.g. http://arashrai.com:5000/randomSEwebsite?omit=Arash will omit my website
        websites.pop(omit, None)  # passing None masks KeyErrors
        lucker_dog = random.choice(list(websites.values()))
        return redirect(lucker_dog, code=302)


class login(Resource):
    def post(self):
        content = request.get_json()
        cur.execute("""SELECT password FROM users
                       WHERE username = %s""", [content["username"]])
        data = cur.fetchall()
        if not data:
            return False
        elif data[0][0] == content["password"]:
            return True
        return False


class signup(Resource):
    def post(self):
        content = request.get_json()
        survey = content["survey"]
        sql = "INSERT INTO surveys (question_one, question_two) VALUES('%s', '%s')" % \
            (survey["question_one"], survey["question_two"])
        cur.execute(sql)
        db.commit()
        cur.execute("""SELECT LAST_INSERT_ID()""")
        data = cur.fetchall()
        sql = "INSERT INTO users (username, password, email, survey_id) VALUES ('%s' ,'%s' ,'%s' , %d)" % \
            (content["username"], content["password"], content["email"], int(data[0][0]))
        try:
            cur.execute(sql)
        except:
            return False
        db.commit()
        return True


api.add_resource(login, '/login')
api.add_resource(signup, '/signup')
api.add_resource(randomSEwebsite, '/randomSEwebsite')

app.register_blueprint(main)
socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
