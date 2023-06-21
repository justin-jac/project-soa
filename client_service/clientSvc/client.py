from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from flask_cors import CORS
from client_producer import *

db = mysql.connector.connect(host="ClientSQL", user="root", password="root",database="client")
dbc = db.cursor(dictionary=True)

def connect():
    db = mysql.connector.connect(host="ClientSQL", user="root", password="root",database="client")
    dbc = db.cursor(dictionary=True)
    return db, dbc

app = Flask(__name__)
CORS(app)

@app.route('/organizer/client', methods = ['POST', 'GET'])
def client():
    db, dbc = connect()
    replyEx_mq = ''
    status_code = 405

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM clients"
        dbc.execute(sql)
        data_client = dbc.fetchall()

        if data_client != None:
            status_code = 200  # The request has succeeded
            replyEx_mq = json.dumps(data_client)

        else: 
            status_code = 404  # No resources found

    # HTTP method = POST
    elif HTTPRequest.method == 'POST':
        try:
            data = json.loads(HTTPRequest.get_data())
            print(f"Received data: {data}")  # Add this debug statement
            # Rest of the code
        except json.decoder.JSONDecodeError as e:
            # Handle the JSON decoding error
            # You can print an error message or return an appropriate response
            status_code = 400  # Bad Request
            replyEx_mq = "Invalid JSON data: " + str(e)
        clientEmail = data["email"]
        clientName = data["nama"]
        contact = data["contact_person"]
        clientPass = data["password"]

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO clients (email, nama, contact_person, password) VALUES (%s,%s,%s,%s)"
            dbc.execute(sql, [clientEmail, clientName, contact, clientPass] )
            db.commit()

            new_client_id = dbc.lastrowid
            dataEx_mq = {}
            dataEx_mq["event"] = "client.new"
            dataEx_mq["id"] = new_client_id
            dataEx_mq["nama"] = clientName
            dataEx_mq["password"] = clientPass
            dataEx_mq["user_status"] = "Client"
            
            mssg_mq = json.dumps(dataEx_mq)

            publish_message(mssg_mq, "client.new")
            
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





@app.route('/organizer/client/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def client2(id):
    db, dbc = connect()
    replyEx_mq = ''
    status_code = 405

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data client
            sql = "SELECT * FROM clients WHERE id = %s"
            dbc.execute(sql, [id])
            data_client = dbc.fetchone()
            if data_client != None:
                replyEx_mq = json.dumps(data_client)
                status_code = 200  # The request has succeeded
            else: 
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request

    # HTTP method = POST
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        clientEmail = data['email']
        clientName = data['nama']
        contact = data['contact_person']
        clientPass = data['password']

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO clients (id, email, nama, contact_person, password) VALUES (%s,%s,%s,%s,%s)"
            dbc.execute(sql, [id,clientEmail,clientName,contact,clientPass] )
            db.commit()
            # dapatkan ID dari data client yang baru dimasukkan
            new_client_id = dbc.lastrowid
            data_client = {'id':new_client_id}
            replyEx_mq = json.dumps(data_client)

            # TODO: Kirim message ke order_service melalui RabbitMQ tentang adanya data client baru


            status_code = 201
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409

    # HTTP method = PUT
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)
         
        clientEmail = data['email']
        clientName = data['nama']
        contact = data['contact_person']
        clientPass = data['password']

        messagelog = 'PUT id: ' + str(id) + ' | nama: ' + clientName + ' | email: ' + clientEmail
        logging.warning("Received: %r" % messagelog)

        try:
            # ubah nama kantin dan gedung di database
            sql = "UPDATE client set email=%s, nama=%s, contact_person=%s, password=%s where id=%s"
            dbc.execute(sql, [clientEmail, clientName, contact, clientPass,id] )
            db.commit()

            # teruskan json yang berisi perubahan data client yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'client.tenant.changed'
            dataEx_mq = {}
            dataEx_mq['event']  = "client.update"
            dataEx_mq['id']     = id
            dataEx_mq['nama']   = clientName
            dataEx_mq['password'] = clientPass
            dataEx_mq['user_status'] = "Client"
            mssg_mq = json.dumps(dataEx_mq)

            publish_message(mssg_mq, "client.update")
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
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





