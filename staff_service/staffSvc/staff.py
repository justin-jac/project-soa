from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from flask_cors import CORS
from staff_producer import *


db = mysql.connector.connect(host="staffSQL", user="root", password="root",database="staff")
dbc = db.cursor(dictionary=True)

def connect():
    db = mysql.connector.connect(host="staffSQL", user="root", password="root",database="staff")
    dbc = db.cursor(dictionary=True)
    return db, dbc

app = Flask(__name__)
CORS(app)

@app.route('/organizer/staf', methods = ['POST', 'GET'])
def staf():
    db , dbc = connect()
    replyEx_mq = ''
    status_code = 405

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM stafs"
        dbc.execute(sql)
        data_staff = dbc.fetchall()

        if data_staff != None:
            status_code = 200  # The request has succeeded
            replyEx_mq = json.dumps(data_staff)

        else: 
            status_code = 404  # No resources found

    # HTTP method = POST

    elif HTTPRequest.method == 'POST':
        try:
            data = json.loads(HTTPRequest.data)
            print(f"Received data: {data}")  # Add this debug statement
            # Rest of the code
        except json.decoder.JSONDecodeError as e:
            # Handle the JSON decoding error
            # You can print an error message or return an appropriate response
            status_code = 400  # Bad Request
            replyEx_mq = "Invalid JSON data: " + str(e)
        staffEmail = data["email"]
        staffName = data["nama"]
        staffPass = data["password"]

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO stafs (email, nama, password) VALUES (%s,%s,%s)"
            dbc.execute(sql, [staffEmail, staffName, staffPass] )
            db.commit()
            
            new_staff_id = dbc.lastrowid
            dataEx_mq = {}
            dataEx_mq["event"] = "staff.new"
            dataEx_mq["id"] = new_staff_id
            dataEx_mq["nama"] = staffName
            dataEx_mq["password"] = staffPass
            dataEx_mq["user_status"] = "Staff"
            
            mssg_mq = json.dumps(dataEx_mq)

            # publish_message(mssg_mq, "staff.new")
            
            # replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staf
    # ------------------------------------------------------
    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





@app.route('/organizer/staf/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def staf2(id):
    db, dbc = connect()   
    replyEx_mq = ''
    status_code= 405

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data staf
            sql = "SELECT * FROM stafs WHERE id = %s"
            dbc.execute(sql, [id])
            data_staff = dbc.fetchone()
            # kalau data staf ada, juga ambil menu dari staf tsb.
            if data_staff != None:
                replyEx_mq = json.dumps(data_staff)
                status_code = 200  # The request has succeeded
            else: 
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request

    # HTTP method = POST
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        staffEmail = data["email"]
        staffName = data["nama"]
        staffPass = data["password"]

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO stafs (id, email, nama, password) VALUES (%s,%s,%s,%s)"
            dbc.execute(sql, [id,staffEmail,staffName,staffPass] )
            db.commit()
            # dapatkan ID dari data staf yang baru dimasukkan
            dataEx_mq = {}
            dataEx_mq["event"] = "staff.new"
            dataEx_mq["id"] = id
            dataEx_mq["nama"] = staffName
            dataEx_mq["password"] = staffPass
            dataEx_mq["user_status"] = "Staff"
            
            mssg_mq = json.dumps(dataEx_mq)

            # publish_message(mssg_mq, "staff.new")
            
            # replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409

    # HTTP method = PUT
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)
         
        staffEmail = data["email"]
        staffName = data["nama"]
        staffPass = data["password"]

        messagelog = 'PUT id: ' + str(id) + ' | nama: ' + staffName + ' | email: ' + staffEmail
        logging.warning("Received: %r" % messagelog)

        try:
            # ubah nama kantin dan gedung di database
            sql = "UPDATE staf set email=%s, nama=%s, password=%s where id=%s"
            dbc.execute(sql, [staffEmail, staffName, staffPass,id] )
            db.commit()

            # teruskan json yang berisi perubahan data staf yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'staf.tenant.changed'
            data_baru = {}
            data_baru["event"]  = "staff_update"
            data_baru["id"]     = id
            # data_baru['email']   = staffEmail
            data_baru["nama"]   = staffName
            data_baru["password"] = staffPass
            replyEx_mq = json.dumps(data_baru)
            publish_message(replyEx_mq,'staff.update')

            status_code = 200
        # bila ada kesalahan saat ubah data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # HTTP method = DELETE
    # ------------------------------------------------------
    elif HTTPRequest.method == 'DELETE':
        data = json.loads(HTTPRequest.data)

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staf
    # ------------------------------------------------------
    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





