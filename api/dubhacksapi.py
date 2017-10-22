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
from itertools import combinations


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
api = Api(app)
app.debug = True
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# main = Blueprint('main', __name__)

db = MySQLdb.connect(host="localhost", user="root",
                     passwd="root", db="DubHacks2017")
cur = db.cursor()

LFP = set()

mapScore = {
    'Strongly Agree': 1,
    'Agree': 2,
    'Neutral': 3,
    'Disagree': 4,
    'Strongly Disagree': 5
}


def background_thread():
    """Example of how to send server generated events to clients."""
    global LFP
    while True:
        socketio.sleep(3)
        print("in background_thread", LFP)
        mock = find_match()
        if mock:
            x = str(random.randint(1, 10**7))
            socketio.emit('joinroom', {'room': x, 'user1': mock[0], 'user2': mock[1], 'common': mock[2], 'controversy': mock[3]}, namespace='/chat')
            print("emitted")


def find_match():
    global LFP
    if len(LFP) < 2:
        return False
    possibilities = list(combinations(LFP, 2))

    scores = []

    for pair in possibilities:
        n = calculate_score(pair[0], pair[1])
        scores.append(n)

#     SELECT * FROM users JOIN surveys ON users.survey_id = surveys.id
# WHERE users.username = 'testuser';
    scores.sort()
    pair = scores[-1]
    LFP = LFP - set([pair[1], pair[2]])
    return (pair[1], pair[2], pair[3], pair[4])


def calculate_score(a, b):
    sql = """
            SELECT * FROM users JOIN surveys ON users.survey_id = surveys.id
            WHERE users.username = %s
          """
    cur.execute(sql, [a])
    data1 = cur.fetchall()
    cur.execute(sql, [b])
    data2 = cur.fetchall()

    common = []
    contro = []
    score = 0

    for x in range(6, 12):
        if data1[0][x] == data2[0][x]:
            score += 1
            common.append(data1[0][x])

    for x in range(12, 16):
        diff = abs(mapScore[data1[0][x]] - mapScore[data2[0][x]])
        score += diff
        if diff > 2:
            contro.append((diff, data1[0], data2[0], x))

    commonString = "You have "

    for x in common:
        commonString += x
        commonString += ", "

    commonString += " and probably much more!"

    contro.sort()
    c = contro[-1]

    controString = a
    controString += "something "
    controString += " "

    print(commonString)
    print(controString)
    return (score, a, b, commonString, controString)


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Chatroom')


@socketio.on('lookingforgroup', namespace='/chat')
def lookingforgroup(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    # session['username'] = message['username']
    # session['room'] = message['username']
    print("in looking for group", message['username'])
    # room = session.get('room')
    # join_room(room)
    LFP.add(message['username'])

    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('revealcontroversy', namespace='/chat')
def revealcontroversy(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    # session['username'] = message['username']
    # session['room'] = message['username']
    print("in looking for group", message['username'])
    # room = session.get('room')
    room = message['room']
    emit('decrementshow', {'room': room, 'username': message['username']}, room=room)


@socketio.on('actuallyjoinroom', namespace='/chat')
def actuallyjoinroom(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print("in actuallyjoinroom")
    room = message['room']
    # # leave_room(message['username'])
    join_room(room)
    # print(room, message['username'])
    sleep(1)
    emit('status', {'msg': message['username'] + ' has entered the room.', 'room': room, 'username': message['username']}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message['room']
    print("getting text", message['username'], room, message['msg'])
    emit('message', {'msg': message['msg'], 'username': message['username'], 'room': room}, room=room)


@socketio.on('connect', namespace='/chat')
def chat():
    print("in connect")
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


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
        sql = "INSERT INTO surveys (musician, born, hobbies, movie, job, superhero, climate, military, abortion, trump) \
            VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
            (survey["musician"], survey["born"], survey["hobbies"], survey["movie"], survey["job"], survey["superhero"], survey["climate"], survey["military"], survey["abortion"], survey["trump"])
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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
