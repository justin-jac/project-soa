from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector
import mysql.connector, json, pika, logging
from flask_cors import CORS
from event_producer import *


db = mysql.connector.connect(host="EventSQL", user="root", password="root",database="eventdb")
dbc = db.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)


@app.route('/eo/event', methods = ['POST', 'GET'])
def event():
    db = mysql.connector.connect(host="EventSQL", user="root", password="root", database="eventdb")
    dbc = db.cursor(dictionary=True)
    reply_req = ''
    status_code = 405

    #region GET /event
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data kantin
        sql = "SELECT * FROM events"
        dbc.execute(sql)
        data_event = dbc.fetchall()

        if data_event != None:
            status_code = 200  # The request has succeeded
            reply_req = json.dumps(data_event, default=str)
        else:
            status_code = 404  # No resources found
    #endregion

    #region POST /event
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)

        id_order = data['idOrder']
        id_pic = data['idStaffPIC']
        nama_event = data['namaEvent']
        desk_event = data['deskripsiEvent']
        tanggal_event = data['tanggalEvent']
        jam_mulai = data['jamMulaiEvent']
        jam_akhir = data['jamAkhirEvent']
        sub_total = data['subTotalEvent']

        try:
            sql = "INSERT INTO events (idOrder, idStaffPIC, namaEvent, deskripsiEvent, tanggalEvent, jamMulaiEvent, "\
                "jamAkhirEvent, subTotalEvent)  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"

            dbc.execute(sql, [id_order, id_pic, nama_event, desk_event, tanggal_event, jam_mulai, jam_akhir, sub_total])
            db.commit()

            new_idEvent = dbc.lastrowid

            data_mq = {}
            data_mq['event'] = "event.new"
            data_mq['idEvent'] = new_idEvent
            data_mq['idOrder'] = id_order
            data_mq['idStaffPIC'] = id_pic
            data_mq['namaEvent'] = nama_event
            data_mq['deskripsiEvent'] = desk_event
            data_mq['tanggalEvent'] = tanggal_event
            data_mq['jamMulaiEvent'] = jam_mulai
            data_mq['jamAkhirEvent'] = jam_akhir
            data_mq['subTotalEvent'] = sub_total
            mssg_mq = json.dumps(data_mq)

            publish_message(mssg_mq, "event.new")

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


@app.route('/eo/event/<path:id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def event2(id):
    db = mysql.connector.connect(host="EventSQL", user="root", password="root", database="eventdb")
    dbc = db.cursor(dictionary=True)
    reply_req = ''
    status_code = 405

    #region GET /event/id
    if HTTPRequest.method == 'GET':
        if id.isnumeric():
            sql = "SELECT * FROM events WHERE idEvent = %s"
            dbc.execute(sql, [id])
            data_event = dbc.fetchone()

            if data_event != None:
                reply_req = json.dumps(data_event, default=str)
                status_code = 200  # The request has succeeded
            else:
                status_code = 404  # No resources found
        else: status_code = 400  # Bad Request
    #endregion

    #region PUT /event/id
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)

        id_order = data['idOrder']
        id_pic = data['idStaffPIC']
        nama_event = data['namaEvent']
        desk_event = data['deskripsiEvent']
        tanggal_event = data['tanggalEvent']
        jam_mulai = data['jamMulaiEvent']
        jam_akhir = data['jamAkhirEvent']
        sub_total = data['subTotalEvent']

        messagelog = 'PUT id: ' + str(id)
        logging.warning("Received: %r" % messagelog)

        try:
            sql = "UPDATE events SET idOrder=%s, idStaffPIC=%s, namaEvent=%s, deskripsiEvent=%s, tanggalEvent=%s, " \
                  "jamMulaiEvent=%s, jamAkhirEvent=%s, subTotalEvent=%s WHERE idEvent=%s"
            dbc.execute(sql, [id_order, id_pic, nama_event, desk_event, tanggal_event, jam_mulai, jam_akhir, sub_total,id])
            db.commit()

            data_mq = {}
            data_mq["event"] = "event.update"
            data_mq["idEvent"] = id
            data_mq['idOrder'] = id_order
            data_mq['idStaffPIC'] = id_pic
            data_mq['namaEvent'] = nama_event
            data_mq['deskripsiEvent'] = desk_event
            data_mq['tanggalEvent'] = tanggal_event
            data_mq['jamMulaiEvent'] = jam_mulai
            data_mq['jamAkhirEvent'] = jam_akhir
            data_mq['subTotalEvent'] = sub_total
            mssg_mq = json.dumps(data_mq)

            publish_message(mssg_mq, "event.update")

            reply_req = json.dumps(data_mq)
            status_code = 200

        except mysql.connector.Error as err:
            status_code = 409
    #endregion

    #region DELETE /event/id
    elif HTTPRequest.method == 'DELETE':
        # data = json.loads(HTTPRequest.data)
        if id.isnumeric():
            sql = "DELETE FROM events WHERE idEvent = %s"
            dbc.execute(sql, [id])
            db.commit()

            data_mq = {}
            data_mq['event'] = "event.delete"
            data_mq['idEvent'] = id
            mssg_mq = json.dumps(data_mq)

            publish_message(mssg_mq, "event.delete")

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
