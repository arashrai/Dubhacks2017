from flask import Flask, redirect, request
from flask_restful import Resource, Api
from flask_cors import CORS
import random
import MySQLdb
import socketio

async_mode = None

db = MySQLdb.connect(host="localhost", user="root",
                     passwd="root", db="DubHacks2017")
cur = db.cursor()

app = Flask(__name__)
CORS(app)
api = Api(app)
sio = socketio.Server(logger=True, async_mode=async_mode)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
thread = None


@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)


@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
