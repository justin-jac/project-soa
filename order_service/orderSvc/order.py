from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import mysql.connector, json, pika, logging
from flask_cors import CORS
# from kantin_producer import *

db = mysql.connector.connect(host="localhost", user="root", password="", database="eventorder")
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


@app.route('/order', methods = ['POST', 'GET'])
def order():
    jsondoc = ''

    #region GET Order
    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM orders"
        dbc.execute(sql)
        data_orders = dbc.fetchall()

        if data_orders != None:
            for order in data_orders:
                order['order_date'] = str(order['order_date'])
            # kalau data order ada, juga ambil menu dari kantin tsb.
            # for x in range(len(data_orders)):
            #     kantin_id = data_orders[x]['id']
            #     sql = "SELECT * FROM orders WHERE idresto = %s"
            #     dbc.execute(sql, [kantin_id])
            #     data_menu = dbc.fetchall()
            #     data_orders[x]['produk'] = data_menu

            status_code = 200  # The request has succeeded
            jsondoc = json.dumps(data_orders)

        else:
            status_code = 404  # No resources found
    #endregion

    #region POST Order
    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        id_client = data["id_client"]
        order_name = data["order_name"]
        order_description = data["order_description"]
        order_date = data["order_date"]
        total_price = data["total_price"]
        status = data["status"]

        try:
            # simpan nama kantin, dan gedung ke database

            sql = "INSERT INTO orders (id_client, order_name,order_description, order_date, total_price, status) " \
                  "VALUES (%s,%s,%s,%s,%s,%s)"

            dbc.execute(sql, [id_client, order_name, order_description, order_date, total_price, status])
            db.commit()

            # dapatkan ID dari data kantin yang baru dimasukkan
            id_order = dbc.lastrowid
            data_orders = {'id':id_order}
            jsondoc = json.dumps(data_orders)

            # simpan menu-menu untuk kantin di atas ke database
            # for i in range(len(data['produk'])):
            #     menu = data['produk'][i]['menu']
            #     price = data['produk'][i]['price']
            #
            #     sql = "INSERT INTO kantin_menu (idresto,menu,price) VALUES (%s,%s,%s)"
            #     dbc.execute(sql, [id_order,menu,price] )
            #     db.commit()


            # Publish event "new kantin" yang berisi data kantin yg baru.
            # Data json yang dikirim sebagai message ke RabbitMQ adalah json asli yang
            # diterima oleh route /kantin [POST] di atas dengan tambahan 2 key baru,
            # yaitu 'event' dan id_order.
            # data['event']  = 'new_order'
            # data['order_id'] = id_order
            # message = json.dumps(data)
            # publish_message(message,'kantin.tenant.new')


            status_code = 201
        # bila ada kesalahan saat insert data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409
    #endregion

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp


@app.route('/order/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def order2(id):
    jsondoc = ''


    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data kantin
            sql = "SELECT * FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id])
            data_order = dbc.fetchone()


            if data_order != None:
                jsondoc = json.dumps(data_order, default=str)
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

        id_client = data["id_client"]
        order_name = data["order_name"]
        order_description = data["order_description"]
        order_date = data["order_date"]
        total_price = data["total_price"]
        status = data["status"]

        # id = data['id']
        # nama = data['nama']
        # gedung = data['gedung']

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            # ubah nama kantin dan gedung di database
            sql = "UPDATE orders SET id_client=%s, order_name=%s, order_description=%s, order_date=%s, " \
                  "total_price=%s, status=%s WHERE id_order=%s"
            dbc.execute(sql, [id_client,order_name, order_description, order_date, total_price,status,id])
            db.commit()

            # teruskan json yang berisi perubahan data kantin yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'kantin.tenant.changed'
            new_data = {}
            new_data['event']  = "updated_order"
            new_data['id']     = id
            jsondoc = json.dumps(new_data)
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
            sql = "DELETE FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id])
            db.commit()

            new_data = {}
            new_data['event']  = "deleted_order"
            new_data['id']     = id
            jsondoc = json.dumps(new_data)
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





