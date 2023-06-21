from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from event_producer import *

db = mysql.connector.connect(host="EventSQL", user="root", password="root",database="event")
dbc = db.cursor(dictionary=True)

app = Flask(__name__)

@app.route('/organizer/event', methods = ['POST', 'GET'])
def event():
    replyEx_mq = ''
    status_code = 405

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
            status_code = 200  # The request has succeeded
            replyEx_mq = json.dumps(data_event, default=str)
        else:
            status_code = 404  # No resources found


    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        id_order = data['id_order']
        id_staff = data['id_staffPIC']
        event_name = data['event_name']
        event_description = data['event_description']
        start_time = data['start_time']
        end_time = data['end_time']
        sub_total = data['sub_total']

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "INSERT INTO events (id_order, id_staffPIC, event_name, event_description, start_time, "\
                "end_time, sub_total)  VALUES  (%s,%s,%s,%s,%s,%s,%s)"

            # sql = "INSERT INTO events (nama,gedung) VALUES (%s,%s)"
            dbc.execute(sql, [id_order, id_staff, event_name, event_description, start_time, end_time, sub_total])
            db.commit()

            new_id_event = dbc.lastrowid
            
            # dataEx_mq = {}
            # dataEx_mq['event'] = "event.new"
            # dataEx_mq['id_event'] = new_id_event
            # dataEx_mq['id_order'] = id_order
            # dataEx_mq['id_staffPIC'] = id_staff
            # dataEx_mq['event_name'] = event_name
            # dataEx_mq['event_description'] = event_description
            # dataEx_mq['start_time'] = start_time
            # dataEx_mq['end_time'] = end_time
            # dataEx_mq['sub_total'] = sub_total
            # msgEx_mq = json.dumps(data_event)
            
            # publish_message(msgEx_mq, "event.new")
            
            # replyEx_mq = json.dumps(dataEx_mq)
            status_code = 201
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


@app.route('/organizer/event/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def event2(id):
    replyEx_mq = ''
    status_code = 405

    # ------------------------------------------------------
    # HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            sql = "SELECT * FROM events WHERE id_event = %s"
            dbc.execute(sql, [id])
            data_event = dbc.fetchone()

            if data_event != None:
                replyEx_mq = json.dumps(data_event, default=str)
                status_code = 200  # The request has succeeded
            else:
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request

    # HTTP method = PUT
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)

        id_order = data['id_order']
        id_staff = data['id_staffPIC']
        event_name = data['event_name']
        event_description = data['event_description']
        start_time = data['start_time']
        end_time = data['end_time']
        sub_total = data['sub_total']

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            sql = "UPDATE events SET id_order=%s, id_staffPIC=%s, event_name=%s, event_description=%s, " \
                  "start_time=%s, end_time=%s, sub_total=%s WHERE id_event=%s"
            dbc.execute(sql, [id_order, id_staff, event_name, event_description, start_time, end_time, sub_total,id])
            db.commit()
            
            # dataEx_mq = {}
            # dataEx_mq['event'] = "event.update"
            # dataEx_mq['id_event'] = id
            # dataEx_mq['id_order'] = id_order
            # dataEx_mq['id_staffPIC'] = id_staff
            # dataEx_mq['event_name'] = event_name
            # dataEx_mq['event_description'] = event_description
            # dataEx_mq['event_date'] = event_date
            # dataEx_mq['start_time'] = start_time
            # dataEx_mq['end_time'] = end_time
            # dataEx_mq['sub_total'] = sub_total
            # msgEx_mq = json.dumps(data_event)
            
            # publish_message(msgEx_mq, "event.update")

            # msgEx_mq = json.dumps(dataEx_mq)

            status_code = 200
        except mysql.connector.Error as err:
            status_code = 409

    # HTTP method = DELETE
    elif HTTPRequest.method == 'DELETE':
        if id.isnumeric():
            sql = "DELETE FROM events WHERE id_event = %s"
            dbc.execute(sql, [id])
            db.commit()

            dataEx_mq = {}
            # dataEx_mq['event']  = "event_delete"
            # dataEx_mq['id']     = id
            # dataEx_mq = json.dumps(dataEx_mq)
            
            # publish_message(msgEx_mq, "event.update")

            msgEx_mq = json.dumps(dataEx_mq)
            
            status_code = 200  # The request has succeeded

        else: status_code = 400  # Bad Request


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if msgEx_mq !='': resp.response = msgEx_mq
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp
