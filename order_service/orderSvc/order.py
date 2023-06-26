from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import mysql.connector, json, pika, logging
from flask_cors import CORS
from order_producer import *

db = mysql.connector.connect(host="OrderSQL", user="root", password="root", database="eventorder")
dbc = db.cursor(dictionary=True)

def connect():
    db = mysql.connector.connect(host="OrderSQL", user="root", password="root", database="eventorder")
    dbc = db.cursor(dictionary=True)
    return db, dbc

app = Flask(__name__)
CORS(app)

@app.route('/organizer/order', methods = ['POST', 'GET'])
def order():
    db = mysql.connector.connect(host="OrderSQL", user="root", password="root", database="eventorder")
    dbc = db.cursor(dictionary=True)
    replyEx_mq = ''
    status_code = 405
    
    #region GET Order
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        sql = "SELECT * FROM orders"
        dbc.execute(sql)
        data_orders = dbc.fetchall()

        if data_orders != None:
            status_code = 200  # The request has succeeded
            replyEx_mq = json.dumps(data_orders, default=str)
        else:
            status_code = 404  # No resources found
    #endregion

    #region POST Order
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        id_client = data["id_client"]
        order_name = data["order_name"]
        order_description = data["order_description"]
        order_date = data["order_date"]
        total_price = data["total_price"]
        status = data["status"]

        try:
            sql = "INSERT INTO orders (id_client, order_name,order_description, order_date, total_price, status) " \
                  "VALUES (%s,%s,%s,%s,%s,%s)"

            dbc.execute(sql, [id_client, order_name, order_description, order_date, total_price, status])
            db.commit()

            new_id_order = dbc.lastrowid
            
            dataEx_mq = {}
            dataEx_mq['event'] = "order.new"
            dataEx_mq['id_order'] = new_id_order
            dataEx_mq['id_client'] = id_client
            dataEx_mq['order_name'] = order_name
            dataEx_mq['order_description'] = order_description
            dataEx_mq['order_date'] = order_date
            dataEx_mq['total_price'] = total_price
            dataEx_mq['status'] = status
            # mssg_mq = json.dumps(dataEx_mq)

            # publish_message(mssg_mq, "order.new")
            
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 201
        except mysql.connector.Error as err:
            status_code = 409
    #endregion

    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp


@app.route('/organizer/order/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def order2(id):
    db , dbc = connect()
    replyEx_mq = ''
    status_code = 405

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data kantin
            sql = "SELECT * FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id])
            data_order = dbc.fetchall()


            if data_order != None:
                replyEx_mq = json.dumps(data_order, default=str)
                status_code = 200  # The request has succeeded
            else:
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request

    # HTTP method = PUT
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)

        id_client = data["id_client"]
        order_name = data["order_name"]
        order_description = data["order_description"]
        order_date = data["order_date"]
        total_price = data["total_price"]
        status = data["status"]

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
            dataEx_mq = {}
            dataEx_mq['event'] = "order.update"
            dataEx_mq['id_order'] = id
            dataEx_mq['id_client'] = id_client
            dataEx_mq['order_name'] = order_name
            dataEx_mq['order_description'] = order_description
            dataEx_mq['order_date'] = order_date
            dataEx_mq['total_price'] = total_price
            dataEx_mq['status'] = status
            mssg_mq = json.dumps(dataEx_mq)

            publish_message(mssg_mq, "order.update")
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200
        except mysql.connector.Error as err:
            status_code = 409

    # HTTP method = DELETE
    elif HTTPRequest.method == 'DELETE':
        # data = json.loads(HTTPRequest.data)
        if id.isnumeric():
            #Delete Orders
            sql = "DELETE FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id])
            db.commit()
            
            #Delete order_events
            sql = "DELETE FROM order_events WHERE id_order = %s"
            dbc.execute(sql, [id])
            db.commit()

            dataEx_mq = {}
            dataEx_mq['event']  = "order.delete"
            dataEx_mq['id']     = id
            mssg_mq = json.dumps(dataEx_mq)
            
            publish_message(mssg_mq, "order.delete")
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200  # The request has succeeded

        else: status_code = 400  # Bad Request

    # Kirimkan JSON yang sudah dibuat ke client
    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp

@app.route('/organizer/order/user/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def order3(id):
    db , dbc = connect()
    replyEx_mq = ''
    status_code = 405

    # HTTP method = GET
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            # ambil data kantin
            sql = "SELECT * FROM orders WHERE id_client = %s"
            dbc.execute(sql, [id])
            data_order = dbc.fetchall()


            if data_order != None:
                replyEx_mq = json.dumps(data_order, default=str)
                status_code = 200  # The request has succeeded
            else:
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request

    # HTTP method = POST
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        order_name = data["order_name"]
        order_description = data["order_description"]
        order_date = data["order_date"]

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            # tambah data ke order
            sql = "INSERT INTO orders (id_client, order_name,order_description, order_date, total_price, status) " \
                  "VALUES (%s,%s,%s,%s,0,'Pending')"
            dbc.execute(sql, [id,order_name, order_description, order_date])
            db.commit()

            # teruskan json yang berisi perubahan data kantin yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'kantin.tenant.changed'
            dataEx_mq = {}
            dataEx_mq['event'] = "order.new"
            dataEx_mq['id_order'] = dbc.lastrowid
            dataEx_mq['id_client'] = id
            dataEx_mq['order_name'] = order_name
            dataEx_mq['order_description'] = order_description
            dataEx_mq['order_date'] = order_date
            mssg_mq = json.dumps(dataEx_mq)

            publish_message(mssg_mq, "order.new")
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200
        except mysql.connector.Error as err:
            status_code = 409

    # HTTP method = PUT
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)

        id_order = data["id_order"]
        order_name = data["order_name"]
        order_description = data["order_description"]
        order_date = data["order_date"]

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            # ubah nama kantin dan gedung di database
            sql = "UPDATE orders SET id_order=%s, order_name=%s, order_description=%s, order_date=%s, " \
                  "WHERE id_client=%s"
            dbc.execute(sql, [id_order,order_name, order_description, order_date, id])
            db.commit()

            # teruskan json yang berisi perubahan data kantin yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'kantin.tenant.changed'
            dataEx_mq = {}
            dataEx_mq['event'] = "order.update"
            dataEx_mq['id_order'] = id_order
            dataEx_mq['id_client'] = id
            dataEx_mq['order_name'] = order_name
            dataEx_mq['order_description'] = order_description
            dataEx_mq['order_date'] = order_date
            mssg_mq = json.dumps(dataEx_mq)

            publish_message(mssg_mq, "order.update")
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200
        except mysql.connector.Error as err:
            status_code = 409

    # HTTP method = DELETE
    elif HTTPRequest.method == 'DELETE':
        data = json.loads(HTTPRequest.data)

        id = data["id_order"]
        # data = json.loads(HTTPRequest.data)
        if id.isnumeric():
            #Delete Orders
            sql = "DELETE FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id])
            db.commit()

            dataEx_mq = {}
            dataEx_mq['event']  = "order.delete"
            dataEx_mq['id_order']     = id
            mssg_mq = json.dumps(dataEx_mq)
            
            publish_message(mssg_mq, "order.delete")
            replyEx_mq = json.dumps(dataEx_mq)
            status_code = 200  # The request has succeeded

        else: status_code = 400  # Bad Request

    # Kirimkan JSON yang sudah dibuat ke client
    resp = HTTPResponse()
    if replyEx_mq !='': resp.response = replyEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp



