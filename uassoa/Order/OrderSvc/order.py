from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import mysql.connector, json, pika, logging
from flask_cors import CORS
from order_producer import *

db = mysql.connector.connect(host="OrderSQL", user="root", password="root", database="orderdb")
dbc = db.cursor(dictionary=True)
app = Flask(__name__)
CORS(app)


@app.route('/eo/order', methods = ['POST', 'GET'])
def order():
    db = mysql.connector.connect(host="OrderSQL", user="root", password="root", database="orderdb")
    dbc = db.cursor(dictionary=True)
    reply_req = ''
    status_code = 405

    #region GET /order
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM orders"
        dbc.execute(sql)
        data_orders = dbc.fetchall()

        if data_orders != None:
            status_code = 200  # The request has succeeded
            reply_req = json.dumps(data_orders, default=str)
        else:
            status_code = 404  # No resources found
    #endregion

    #region POST /order
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        id_client = data["idClient"]
        nama_order = data["namaOrder"]
        desk_order = data["deskripsiOrder"]
        tgl_order = data["tanggalOrder"]
        total_order = data["totalHargaOrder"]
        stat_order = data["statusOrder"]

        try:
            sql = "INSERT INTO orders (idClient, namaOrder,deskripsiOrder, tanggalOrder, totalHargaOrder, statusOrder) " \
                  "VALUES (%s,%s,%s,%s,%s,%s)"

            dbc.execute(sql, [id_client, nama_order, desk_order, tgl_order, total_order, stat_order])
            db.commit()

            new_idOrder = dbc.lastrowid

            data_mq = {}
            data_mq["event"] = "order.new"
            data_mq["idOrder"] = new_idOrder
            data_mq["idClient"] = id_client
            data_mq["namaOrder"] = nama_order
            data_mq["deskripsiOrder"] = desk_order
            data_mq["tanggalOrder"] = tgl_order
            data_mq["totalHargaOrder"] = total_order
            data_mq["statusOrder"] = stat_order
            mssg_mq = json.dumps(data_mq)

            # publish_message(mssg_mq, "order.new")
            reply_req = json.dumps(data_mq)
            status_code = 201
        except mysql.connector.Error as err:
            status_code = 409

    resp = HTTPResponse()
    if reply_req !='': resp.response = reply_req
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp
    #endregion


@app.route('/eo/order/<path:id>', methods = ['GET', 'PUT', 'DELETE'])
def order2(id):
    db = mysql.connector.connect(host="OrderSQL", user="root", password="root", database="orderdb")
    dbc = db.cursor(dictionary=True)
    reply_req = ''
    status_code = 405

    #region GET /order/id
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data kantin
            sql = "SELECT * FROM orders WHERE idOrder = %s"
            dbc.execute(sql, [id])
            data_order = dbc.fetchone()

            if data_order != None:
                reply_req = json.dumps(data_order, default=str)
                status_code = 200  # The request has succeeded
            else:
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request
    #endregion

    #region PUT /order/id
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)

        id_client = data["idClient"]
        nama_order = data["namaOrder"]
        desk_order = data["deskripsiOrder"]
        tgl_order = data["tanggalOrder"]
        total_order = data["totalHargaOrder"]
        stat_order = data["statusOrder"]

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            sql = "UPDATE orders SET idClient=%s, namaOrder=%s, deskripsiOrder=%s, tanggalOrder=%s, " \
                  "totalHargaOrder=%s, statusOrder=%s WHERE idOrder=%s"
            dbc.execute(sql, [id_client,nama_order, desk_order, tgl_order, total_order,stat_order,id])
            db.commit()

            # teruskan json yang berisi perubahan data kantin yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'kantin.tenant.changed'
            data_mq = {}
            data_mq["event"] = "order.update"
            data_mq["idOrder"] = id
            data_mq["idClient"] = id_client
            data_mq["namaOrder"] = nama_order
            data_mq["deskripsiOrder"] = desk_order
            data_mq["tanggalOrder"] = tgl_order
            data_mq["totalHargaOrder"] = total_order
            data_mq["statusOrder"] = stat_order
            mssg_mq = json.dumps(data_mq)

            publish_message(mssg_mq, "order.update")

            reply_req = json.dumps(data_mq)
            status_code = 200

        except mysql.connector.Error as err:
            status_code = 409
    #endregion

    #region DELETE /order/id
    elif HTTPRequest.method == 'DELETE':
        # data = json.loads(HTTPRequest.data)
        if id.isnumeric():
            # Delete orders
            sql = "DELETE FROM orders WHERE idOrder = %s"
            dbc.execute(sql, [id])
            db.commit()

            # Delete order_events
            sql = "DELETE FROM order_events WHERE idOrder = %s"
            dbc.execute(sql, [id])
            db.commit()

            data_mq = {}
            data_mq['event'] = "order.delete"
            data_mq['idOrder'] = id
            mssg_mq = json.dumps(data_mq)

            publish_message(mssg_mq, "order.delete")

            reply_req = json.dumps(data_mq)
            status_code = 200  # The request has succeeded
        else:
            status_code = 400  # Bad Request
    #endregion

    resp = HTTPResponse()
    if reply_req !='': resp.response = reply_req
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





