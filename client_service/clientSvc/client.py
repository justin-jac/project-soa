from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from client_producer import *

db = mysql.connector.connect(host="ClientSQL", user="root", password="root",database="client")
dbc = db.cursor(dictionary=True)


app = Flask(__name__)

# Note, HTTP response codes are
#  200 = OK the request has succeeded.
#  201 = the request has succeeded and a new resource has been created as a result.    
#  401 = Unauthorized (user identity is unknown)
#  403 = Forbidden (user identity is known to the server)
#  409 = A conflict with the current state of the resource
#  429 = Too Many Requests


@app.route('/client', methods = ['POST', 'GET'])
def client():
    jsondoc = ''


    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM clients"
        dbc.execute(sql)
        data_client = dbc.fetchall()

        if data_client != None:
        #     # kalau data client ada, juga ambil menu dari client tsb.
        #     for x in range(len(data_client)):
        #         client_id = data_client[x]['id']
        #         sql = "SELECT * FROM client_menu WHERE idresto = %s"
        #         dbc.execute(sql, [client_id])
        #         data_menu = dbc.fetchall()
        #         data_client[x]['produk'] = data_menu

            status_code = 200  # The request has succeeded
            jsondoc = json.dumps(data_client)

        else: 
            status_code = 404  # No resources found


    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        clientEmail = data['email']
        clientName = data['nama']
        contact = data['contact_person']
        clientPass = data['password']

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO clients (email, nama, contact_person, password) VALUES (%s,%s,%s,%s)"
            dbc.execute(sql, [clientEmail, clientName, contact, clientPass] )
            db.commit()
            # dapatkan ID dari data kantin yang baru dimasukkan
            clientID = dbc.lastrowid
            data_client = {'id':clientID}
            jsondoc = json.dumps(data_client)

            # # simpan menu-menu untuk client di atas ke database
            # for i in range(len(data['produk'])):
            #     menu = data['produk'][i]['menu']
            #     price = data['produk'][i]['price']

            #     sql = "INSERT INTO kantin_menu (idresto,menu,price) VALUES (%s,%s,%s)"
            #     dbc.execute(sql, [kantinID,menu,price] )
            #     db.commit()


            # Publish event "new kantin" yang berisi data kantin yg baru.
            # Data json yang dikirim sebagai message ke RabbitMQ adalah json asli yang
            # diterima oleh route /kantin [POST] di atas dengan tambahan 2 key baru,
            # yaitu 'event' dan kantinID.
            data['event']  = 'new_client'
            data['client_id'] = clientID
            message = json.dumps(data)
            publish_message(message,'client.new')


            status_code = 201
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





@app.route('/client/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def client2(id):
    jsondoc = ''


    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data client
            sql = "SELECT * FROM clients WHERE id = %s"
            dbc.execute(sql, [id])
            data_client = dbc.fetchone()
            # kalau data client ada, juga ambil menu dari client tsb.
            if data_client != None:
                # sql = "SELECT * FROM clients WHERE idresto = %s"
                # dbc.execute(sql, [id])
                # data_menu = dbc.fetchall()
                # data_client['produk'] = data_menu
                jsondoc = json.dumps(data_client)

                status_code = 200  # The request has succeeded
            else: 
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request


    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
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
            clientID = dbc.lastrowid
            data_client = {'id':clientID}
            jsondoc = json.dumps(data_client)

            # TODO: Kirim message ke order_service melalui RabbitMQ tentang adanya data client baru


            status_code = 201
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # HTTP method = PUT
    # ------------------------------------------------------
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
            data_baru = {}
            data_baru['event']  = "updated_tenant"
            data_baru['id']     = id
            data_baru['email']   = clientEmail
            data_baru['nama']   = clientName
            data_baru['contact_person'] = contact
            data_baru['password'] = clientPass
            jsondoc = json.dumps(data_baru)
            publish_message(jsondoc,'client.changed')

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
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





