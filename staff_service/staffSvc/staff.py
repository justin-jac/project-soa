from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from staff_producer import *

db = mysql.connector.connect(host="stafsQL", user="root", password="root",database="staf")
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
        sql = "SELECT * FROM stafs"
        dbc.execute(sql)
        data_staff = dbc.fetchall()

        if data_staff != None:
        #     # kalau data client ada, juga ambil menu dari client tsb.
        #     for x in range(len(data_staff)):
        #         staff_id = data_staff[x]['id']
        #         sql = "SELECT * FROM client_menu WHERE id = %s"
        #         dbc.execute(sql, [staff_id])
        #         data_menu = dbc.fetchall()
        #         data_staff[x]['produk'] = data_menu

            status_code = 200  # The request has succeeded
            jsondoc = json.dumps(data_staff)

        else: 
            status_code = 404  # No resources found


    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
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
            jsondoc = json.dumps(data_staff)

            # # simpan menu-menu untuk client di atas ke database
            # for i in range(len(data['produk'])):
            #     menu = data['produk'][i]['menu']
            #     price = data['produk'][i]['price']

            #     sql = "INSERT INTO kantin_menu (id,menu,price) VALUES (%s,%s,%s)"
            #     dbc.execute(sql, [kantinID,menu,price] )
            #     db.commit()


            # Publish event "new kantin" yang berisi data kantin yg baru.
            # Data json yang dikirim sebagai message ke RabbitMQ adalah json asli yang
            # diterima oleh route /kantin [POST] di atas dengan tambahan 2 key baru,
            # yaitu 'event' dan kantinID.
            data['event']  = 'new_staff'
            data['staff_id'] = staffID
            message = json.dumps(data)
            publish_message(message,'staff.new')


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
            sql = "SELECT * FROM stafs WHERE id = %s"
            dbc.execute(sql, [id])
            data_staff = dbc.fetchone()
            # kalau data client ada, juga ambil menu dari client tsb.
            if data_staff != None:
                # sql = "SELECT * FROM stafs WHERE id = %s"
                # dbc.execute(sql, [id])
                # data_menu = dbc.fetchall()
                # data_staff['produk'] = data_menu
                jsondoc = json.dumps(data_staff)

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
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO stafs (id, email, nama, password) VALUES (%s,%s,%s,%s,%s)"
            dbc.execute(sql, [id,staffEmail,staffName,staffPass] )
            db.commit()
            # dapatkan ID dari data client yang baru dimasukkan
            staffID = dbc.lastrowid
            data_staff = {'id':staffID}
            jsondoc = json.dumps(data_staff)

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
         
        staffEmail = data['email']
        staffName = data['nama']
        staffPass = data['password']

        messagelog = 'PUT id: ' + str(id) + ' | nama: ' + staffName + ' | email: ' + staffEmail
        logging.warning("Received: %r" % messagelog)

        try:
            # ubah nama kantin dan gedung di database
            sql = "UPDATE client set email=%s, nama=%s, password=%s where id=%s"
            dbc.execute(sql, [staffEmail, staffName, staffPass,id] )
            db.commit()

            # teruskan json yang berisi perubahan data client yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'client.tenant.changed'
            data_baru = {}
            data_baru['event']  = "updated_tenant"
            data_baru['id']     = id
            data_baru['email']   = staffEmail
            data_baru['nama']   = staffName
            data_baru['password'] = staffPass
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





