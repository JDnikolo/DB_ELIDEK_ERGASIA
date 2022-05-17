from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector


# configuration
DEBUG = True
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='test'
)
mycursor = mydb.cursor()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    sql = 'SELECT * FROM researcher WHERE sex="other"'
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


if __name__ == '__main__':
    app.run()
