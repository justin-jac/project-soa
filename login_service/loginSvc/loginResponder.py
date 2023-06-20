from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import json
from flask_cors import CORS

db = mysql.connector.connect(host="localhost", user="root", password="root",database="loginservice")
cursor = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

@app.route('/eo/login', methods = ['POST', 'GET'])
def login():
    db = mysql.connector.connect(host="LoginSQL", user="root", password="root",database="loginservice")
    cursor = db.cursor(dictionary=True)
    db = mysql.connector.connect(host="localhost", user="root", password="root",database="loginservice")
    cursor = db.cursor(dictionary=True)
    jsonData = ''
    statusCode = 400
    
    userInfo = json.loads(HTTPRequest.data)
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(sql,[userInfo['username'],userInfo['password']])
    data = cursor.fetchall()
    
    jsonData = json.dumps(data)
    statusCode = 200
    
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp