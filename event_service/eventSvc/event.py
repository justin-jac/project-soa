from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import mysql.connector, json, pika, logging
from flask_cors import CORS
# from kantin_producer import *

db = mysql.connector.connect(host="localhost", user="root", password="",database="event")
dbc = db.cursor(dictionary=True)


app = Flask(__name__)
CORS(app)
# Note, HTTP response codes are
#  200 = OK the request has succeeded.
#  201 = the request has succeeded and a new resource has been created as a result.
#  401 = Unauthorized (user identity is unknown)
#  403 = Forbidden (user identity is known to the server)
#  409 = A conflict with the current state of the resource
#  429 = Too Many Requests


@app.route('/event', methods = ['POST', 'GET'])
def event():
    jsondoc = ''

    #region GET
    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM events"
        dbc.execute(sql)
        data_event = dbc.fetchall()

        if data_event != None:
            # kalau data order ada, juga ambil menu dari kantin tsb.
            # for x in range(len(data_event)):
            #     kantin_id = data_event[x]['id']
            #     sql = "SELECT * FROM orders WHERE idresto = %s"
            #     dbc.execute(sql, [kantin_id])
            #     data_menu = dbc.fetchall()
            #     data_event[x]['produk'] = data_menu

            status_code = 200  # The request has succeeded
            jsondoc = json.dumps(data_event, default=str)
        else:
            status_code = 404  # No resources found
    #endregion

    #region POST
    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        id_order = data['id_order']
        id_staff = data['id_staffPIC']
        event_name = data['event_name']
        event_description = data['event_description']
        event_date = data['event_date']
        start_time = data['start_time']
        end_time = data['end_time']
        sub_total = data['sub_total']

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO events (id_order, id_staffPIC, event_name, event_description, event_date, start_time, "\
                "end_time, sub_total)  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"



            # sql = "INSERT INTO events (nama,gedung) VALUES (%s,%s)"
            dbc.execute(sql, [id_order, id_staff, event_name, event_description, event_date, start_time, end_time, sub_total])
            db.commit()
            # dapatkan ID dari data kantin yang baru dimasukkan
            id_event = dbc.lastrowid
            data_event = {'id':id_event}
            jsondoc = json.dumps(data_event)

            # simpan menu-menu untuk kantin di atas ke database
            # for i in range(len(data['produk'])):
            #     menu = data['produk'][i]['menu']
            #     price = data['produk'][i]['price']
            #
            #     sql = "INSERT INTO kantin_menu (idresto,menu,price) VALUES (%s,%s,%s)"
            #     dbc.execute(sql, [id_event,menu,price] )
            #     db.commit()


            # Publish event "new kantin" yang berisi data kantin yg baru.
            # Data json yang dikirim sebagai message ke RabbitMQ adalah json asli yang
            # diterima oleh route /kantin [POST] di atas dengan tambahan 2 key baru,
            # yaitu 'event' dan id_event.
            data['event']  = 'new_event'
            data['event_id'] = id_event
            message = json.dumps(data)
            # publish_message(message,'kantin.tenant.new')


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
    #endregion


@app.route('/event/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def event2(id):
    jsondoc = ''


    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data kantin
            sql = "SELECT * FROM events WHERE id_event = %s"
            dbc.execute(sql, [id])
            data_event = dbc.fetchone()


            if data_event != None:
                jsondoc = json.dumps(data_event, default=str)
                status_code = 200  # The request has succeeded
            else:
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request


    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    # elif HTTPRequest.method == 'POST':
    #     data = json.loads(HTTPRequest.data)
    #     kantinName = data['nama']
    #     gedung = data['gedung']
    #
    #     try:
    #         # simpan nama kantin, dan gedung ke database
    #         sql = "INSERT INTO kantin_resto (id, nama,gedung) VALUES (%s,%s,%s)"
    #         dbc.execute(sql, [id,kantinName,gedung] )
    #         db.commit()
    #         # dapatkan ID dari data kantin yang baru dimasukkan
    #         kantinID = dbc.lastrowid
    #         data_kantin = {'id':kantinID}
    #         jsondoc = json.dumps(data_kantin)
    #
    #         # TODO: Kirim message ke order_service melalui RabbitMQ tentang adanya data kantin baru
    #
    #
    #         status_code = 201
    #     # bila ada kesalahan saat insert data, buat XML dengan pesan error
    #     except mysql.connector.Error as err:
    #         status_code = 409


    # ------------------------------------------------------
    # HTTP method = PUT
    # ------------------------------------------------------
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)

        id_order = data['id_order']
        id_staff = data['id_staffPIC']
        event_name = data['event_name']
        event_description = data['event_description']
        event_date = data['event_date']
        start_time = data['start_time']
        end_time = data['end_time']
        sub_total = data['sub_total']

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            # ubah nama kantin dan gedung di database
            sql = "UPDATE events SET id_order=%s, id_staffPIC=%s, event_name=%s, event_description=%s, event_date=%s, " \
                  "start_time=%s, end_time=%s, sub_total=%s WHERE id_event=%s"
            dbc.execute(sql, [id_order, id_staff, event_name, event_description, event_date, start_time, end_time, sub_total,id])
            db.commit()

            # teruskan json yang berisi perubahan data kantin yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'kantin.tenant.changed'
            data_baru = {}
            data_baru['event']  = "updated_event"
            data_baru['id']     = id
            jsondoc = json.dumps(data_baru)
            # publish_message(jsondoc,'kantin.tenant.changed')

            status_code = 200
        # bila ada kesalahan saat ubah data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # HTTP method = DELETE
    # ------------------------------------------------------
    elif HTTPRequest.method == 'DELETE':
        # data = json.loads(HTTPRequest.data)
        if id.isnumeric():
            sql = "DELETE FROM events WHERE id_event = %s"
            dbc.execute(sql, [id])
            db.commit()

            data_baru = {}
            data_baru['event']  = "deleted_order"
            data_baru['id']     = id
            jsondoc = json.dumps(data_baru)
            status_code = 200  # The request has succeeded

        else: status_code = 400  # Bad Request


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp
