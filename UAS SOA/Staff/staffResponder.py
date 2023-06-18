from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import json
from flask_cors import CORS
from staff_producer import *

db = mysql.connector.connect(host="localhost", user="root", password="",database="staffdb")
cursor = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

@app.route('/eo/staff/register', methods = ['POST', 'GET'])
def register():
    print("MASOK")
    jsonData = ''
    statusCode = 400
    staffInfo = json.loads(HTTPRequest.data)
    sql = "INSERT INTO staffinfo (namaStaff,usernameStaff,passwordStaff,noTelpStaff,alamatStaff) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(sql,[staffInfo['namaStaff'],
                        staffInfo['userStaff'],
                        staffInfo['passwordStaff'],
                        staffInfo['noTelpStaff'],
                        staffInfo['alamatStaff']])
    lastId = cursor.lastrowid
    db.commit()
    data = {}
    data["event"] = "staff_new"
    data["idUser"] = lastId
    data["username"] = staffInfo['userStaff']
    data["password"] = staffInfo['passwordStaff']
    data["userType"] = "Staff"
    message = json.dumps(data)
    publish_message(message,"staff.new")
    statusCode = 200
    jsonData = json.dumps({'status': "Sukses"})
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp

@app.route('/eo/staff/<path:id>', methods = ['POST', 'GET','PUT'])
def getStaff(id):
    jsonData = ''
    statusCode = 400
    if HTTPRequest.method == 'GET':
        sql = "SELECT * FROM staffinfo WHERE idStaff = %s"
        cursor.execute(sql,[id])
        staffData = cursor.fetchall()
        jsonData = json.dumps(staffData)
        statusCode = 200
    elif HTTPRequest.method == 'PUT':
        staffInfo = json.loads(HTTPRequest.data)
        sql = "UPDATE staffinfo SET namaStaff = %s, usernameStaff = %s, passwordStaff = %s, noTelpStaff = %s, alamatStaff = %s"
        cursor.execute(sql,[staffInfo['namaStaff'],
                        staffInfo['userStaff'],
                        staffInfo['passwordStaff'],
                        staffInfo['noTelpStaff'],
                        staffInfo['alamatStaff']])
        db.commit()
        data = {}
        data["event"] = "staff_update"
        data["idUser"] = id
        data["username"] = staffInfo['userStaff']
        data["password"] = staffInfo['passwordStaff']
        data["userType"] = "Staff"
        message = json.dumps(data)
        publish_message(message,"staff.update")
        statusCode = 200
        jsonData = json.dumps({'status': "Sukses"})
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp

@app.route('/eo/staff', methods = ['POST', 'GET'])
def getAllStaff():
    jsonData = ''
    statusCode = 400
    sql = "SELECT * FROM staffinfo"
    cursor.execute(sql)
    staffData = cursor.fetchall()
    jsonData = json.dumps(staffData)
    statusCode = 200
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp