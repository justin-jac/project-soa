from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import json
from flask_cors import CORS
from client_producer import *

db = mysql.connector.connect(host="localhost", user="root", password="",database="clientdb")
cursor = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

@app.route('/eo/client/register', methods = ['POST', 'GET'])
def register():
    jsonData = ''
    statusCode = 400
    clientInfo = json.loads(HTTPRequest.data)
    sql = "INSERT INTO clientinfo (namaClient,emailClient,passwordClient,noTelpClient,alamatClient) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(sql,[clientInfo['namaClient'],
                        clientInfo['userClient'],
                        clientInfo['passwordClient'],
                        clientInfo['noTelpClient'],
                        clientInfo['alamatClient']])
    lastId = cursor.lastrowid
    db.commit()
    data = {}
    data["event"] = "client_new"
    data["idUser"] = lastId
    data["username"] = clientInfo['userClient']
    data["password"] = clientInfo['passwordClient']
    data["userType"] = "Client"
    message = json.dumps(data)
    publish_message(message,"client.new")
    statusCode = 200
    jsonData = json.dumps({'status': "Sukses"})
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp

@app.route('/eo/client/<path:id>', methods = ['POST', 'GET','PUT'])
def getClient(id):
    jsonData = ''
    statusCode = 400
    if HTTPRequest.method == 'GET':
        sql = "SELECT * FROM clientinfo WHERE clientId = %s"
        cursor.execute(sql,[id])
        clientData = cursor.fetchall()
        jsonData = json.dumps(clientData)
        statusCode = 200
    elif HTTPRequest.method == 'PUT':
        clientInfo = json.loads(HTTPRequest.data)
        sql = "UPDATE staffinfo SET namaClient = %s, emailClient = %s, passwordClient = %s, noTelpClient = %s, alamatClient = %s"
        cursor.execute(sql,[clientInfo['namaClient'],
                            clientInfo['userClient'],
                            clientInfo['passwordClient'],
                            clientInfo['noTelpClient'],
                            clientInfo['alamatClient']])
        db.commit()
        data = {}
        data["event"] = "client_update"
        data["idUser"] = id
        data["username"] = clientInfo['userClient']
        data["password"] = clientInfo['passwordClient']
        data["userType"] = "Client"
        message = json.dumps(data)
        publish_message(message,"client.update")
        statusCode = 200
        jsonData = json.dumps({'status': "Sukses"})
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp

@app.route('/eo/client', methods = ['POST', 'GET'])
def getAllClient():
    jsonData = ''
    statusCode = 400
    sql = "SELECT * FROM clientinfo"
    cursor.execute(sql)
    clientData = cursor.fetchall()
    jsonData = json.dumps(clientData)
    statusCode = 200
    resp = HTTPResponse()
    if jsonData !='': resp.response = jsonData
    resp.headers['Content-Type'] = 'application/json'
    resp.status = statusCode
    return resp