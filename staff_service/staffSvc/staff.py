from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from staff_producer import *

db = mysql.connector.connect(host="stafsQL", user="root", password="root",database="staf")
dbc = db.cursor(dictionary=True)

app = Flask(__name__)

@app.route('/staf', methods = ['POST', 'GET'])
def staf():
    jsondoc = ''

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
            jsondoc = json.dumps(data_staff)

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
            jsondoc = json.dumps(data_staff)

            data['event']  = 'new_staff'
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
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





@app.route('/staf/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def staf2(id):
    jsondoc = ''

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data staf
            sql = "SELECT * FROM stafs WHERE id = %s"
            dbc.execute(sql, [id])
            data_staff = dbc.fetchone()
            # kalau data staf ada, juga ambil menu dari staf tsb.
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
            # dapatkan ID dari data staf yang baru dimasukkan
            staffID = dbc.lastrowid
            data_staff = {'id':staffID}
            jsondoc = json.dumps(data_staff)

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
            # ubah nama kantin dan gedung di database
            sql = "UPDATE staf set email=%s, nama=%s, password=%s where id=%s"
            dbc.execute(sql, [staffEmail, staffName, staffPass,id] )
            db.commit()

            # teruskan json yang berisi perubahan data staf yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'staf.tenant.changed'
            data_baru = {}
            data_baru['event']  = "updated_tenant"
            data_baru['id']     = id
            data_baru['email']   = staffEmail
            data_baru['nama']   = staffName
            data_baru['password'] = staffPass
            jsondoc = json.dumps(data_baru)
            publish_message(jsondoc,'staf.changed')

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
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





