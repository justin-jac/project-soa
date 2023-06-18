from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from staff_producer import *
from flask_cors import CORS

db = mysql.connector.connect(host="stafsQL", user="root", password="root",database="staf")
dbc = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

@app.route('/eo/staf', methods = ['POST', 'GET'])
def staf():
    replyEx_mq = ''
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
        data = json.loads(HTTPRequest.data)
        staffEmail = data['email']
        staffName = data['nama']
        staffPass = data['password']

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO stafs (email, nama, password) VALUES (%s,%s,%s,%s)"
            dbc.execute(sql, [staffEmail, staffName, staffPass] )
            db.commit()
            # dapatkan ID dari data kantin yang baru dimasukkan
            staffID = dbc.lastrowid
            data_staff = {'id':staffID}
            replyEx_mq = json.dumps(data_staff)

            data['event']  = 'staff.new'
            data['staff_id'] = staffID
            message = json.dumps(data)
            publish_message(message,'staff.new')


            status_code = 201
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

@app.route('/eo/staf/register', methods = ['POST', 'GET'])
def register():
    replyEx_mq = ''
    statusCode = 405
    
    data = json.loads(HTTPRequest.data)
    staffEmail = data['email']
    staffName = data['nama']
    staffPass = data['password']
    
    try:
        sql = "INSERT INTO stafs (id, email, nama, password) VALUES (%s,%s,%s,%s,%s)"
        dbc.execute(sql, [staffEmail,staffName,staffPass] )
        db.commit()
        
        new_id_staf = dbc.lastrowid
        
        dataEx_mq = {}
        dataEx_mq['event'] = "staf.new"
        dataEx_mq['id'] = new_id_staf
        dataEx_mq['nama'] = staffName
        dataEx_mq['password'] = staffPass
        dataEx_mq['user_status'] = "Staff"

        mssg_mq = json.dumps(dataEx_mq)

        publish_message(mssg_mq, "staf.new")
        
        replyEx_mq = json.dumps(dataEx_mq)
        status_code = 201
    except mysql.connector.Error as err:
        status_code = 409

    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp
    



@app.route('/eo/staf/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def staf2(id):
    replyEx_mq = ''

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

    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        staffEmail = data['email']
        staffName = data['nama']
        staffPass = data['password']
        try:
            sql = "INSERT INTO stafs (id, email, nama, password) VALUES (%s,%s,%s,%s,%s)"
            dbc.execute(sql, [id,staffEmail,staffName,staffPass] )
            db.commit()
            # dapatkan ID dari data staf yang baru dimasukkan
            staffID = dbc.lastrowid
            data_staff = {'id':staffID}
            replyEx_mq = json.dumps(data_staff)

            # TODO: Kirim message ke order_service melalui RabbitMQ tentang adanya data staf baru


            status_code = 201
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409

    # ------------------------------------------------------
    # HTTP method = PUT
    # ------------------------------------------------------
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)
        staffEmail = data['email']
        staffName = data['nama']
        staffPass = data['password']

        messagelog = 'PUT id: ' + str(id) + ' | nama: ' + staffName + ' | email: ' + staffEmail
        logging.warning("Received: %r" % messagelog)

        try:
            sql = "UPDATE staf set email=%s, nama=%s, password=%s where id=%s"
            dbc.execute(sql, [staffEmail, staffName, staffPass,id] )
            db.commit()
            
            dataEx_mq = {}
            dataEx_mq['event']  = "staf.update"
            dataEx_mq['id']     = id
            dataEx_mq['email']   = staffEmail
            dataEx_mq['nama']   = staffName
            dataEx_mq['password'] = staffPass
            dataEx_mq['user_status'] = "Staff"
            mssg_mq = json.dumps(dataEx_mq)

            publish_message(mssg_mq, "staf.update")
            
            replyEx_mq = json.dumps(dataEx_mq)
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





