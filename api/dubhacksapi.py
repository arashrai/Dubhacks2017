from flask import Flask, request
from flask_restful import Resource, Api
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root",
                     passwd="root", db="DubHacks2017")
cur = db.cursor()

app = Flask(__name__)
api = Api(app)


class login(Resource):
    def post(self):
        content = request.get_json()
        cur.execute("""SELECT password FROM breakfast
                       WHERE username = %s""", (content["username"],))
        data = cur.fetchall()
        if not data:
            return False
        elif data[0][0] == content["password"]:
            return True
        return False


class signup(Resource):
    def post(self):
        content = request.get_json()
        print(content)
        return content["signup"]


api.add_resource(login, '/login')
api.add_resource(signup, '/signup')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
