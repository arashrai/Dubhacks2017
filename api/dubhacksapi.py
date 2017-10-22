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
        for question in survey:
            print(question, survey[question])
        sql = ("""INSERT INTO surveys (question_one, question_two)
                  VALUES (%s , %s)""", [survey["question_one"], survey["question_two"]])
        cur.execute(sql)
        cur.execute("""SELECT LAST_INSERT_ID()""")
        data = cur.fetchall()
        sql = ("""INSERT INTO users (username, password, email, survey_id)
                  VALUES (%s , %s, %s, %d)""", [content["username"], content["password"], content["email"], int(data[0][0])])
        cur.execute(sql)
        return True


api.add_resource(login, '/login')
api.add_resource(signup, '/signup')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
