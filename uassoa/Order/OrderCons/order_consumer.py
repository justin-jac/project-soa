import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="orderdb")
dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):
        data = json.loads(body)
        event = data['event']
        message = "Tidak Merubah Database"

        if event == "event.new":
            new_idEvent = data["idEvent"]
            idOrder = data["idOrder"]
            subtotal = data["subTotalEvent"]

            # Add events
            sql = "INSERT INTO order_events (idEvent, idOrder, subtotal) VALUES (%s,%s,%s)"
            dbc.execute(sql, [new_idEvent, idOrder, subtotal])
            db.commit()

            # Update orders
            sql = "SELECT totalHargaOrder FROM orders WHERE idOrder = %s"
            dbc.execute(sql, [idOrder])
            prev_total = dbc.fetchone()['totalHargaOrder']
            new_total_order = prev_total + subtotal

            sql = "UPDATE orders SET totalHargaOrder=%s WHERE idOrder=%s"
            dbc.execute(sql, [new_total_order, idOrder])
            db.commit()

            message = "Sukses Menambah Total Order "+str(idOrder)+" & Event "+str(new_idEvent)

        elif event == "event.update":
            idEvent = data["idEvent"]
            idOrder = data["idOrder"]
            new_subtotal = data["subTotalEvent"]

            # Get previous subtotal
            sql = "SELECT subtotal FROM order_events WHERE idEvent=%s"
            dbc.execute(sql, [idEvent])
            prev_subtotal = dbc.fetchone()["subtotal"]

            selisih_subtotal = new_subtotal - prev_subtotal

            # Update events
            sql = "UPDATE order_events SET subtotal=%s WHERE idEvent=%s"
            dbc.execute(sql, [new_subtotal, idEvent])
            db.commit()

            # Update orders
            sql = "SELECT totalHargaOrder FROM orders WHERE idOrder = %s"
            dbc.execute(sql, [idOrder])
            prev_total = dbc.fetchone()['totalHargaOrder']
            new_total_order = prev_total + selisih_subtotal

            sql = "UPDATE orders SET totalHargaOrder=%s WHERE idOrder=%s"
            dbc.execute(sql, [new_total_order, idOrder])
            db.commit()

            message = "Sukses Mengubah Total Order "+str(idOrder)+" & Event "+str(idEvent)

        elif event == "event.delete":
            del_idEvent = data["idEvent"]

            # Get idOrder & subtotal
            sql = "SELECT idOrder, subtotal FROM order_events WHERE idEvent=%s"
            dbc.execute(sql, [del_idEvent])
            data_del = dbc.fetchone()
            idOrder = data_del["idOrder"]
            del_subtotal = data_del["subtotal"]

            # DELETE events
            sql = "DELETE FROM order_events WHERE idEvent=%s"
            dbc.execute(sql, [del_idEvent])
            db.commit()

            # Update orders
            sql = "SELECT totalHargaOrder FROM orders WHERE idOrder = %s"
            dbc.execute(sql, [idOrder])
            prev_total = dbc.fetchone()['totalHargaOrder']
            new_total_order = prev_total - del_subtotal

            sql = "UPDATE orders SET totalHargaOrder=%s WHERE idOrder=%s"
            dbc.execute(sql, [new_total_order, idOrder])
            db.commit()

            message = "Sukses Mengurangi Total Order "+str(idOrder)+" & Menghapus Event "+str(del_idEvent)

        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EoMQ', 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='eoExchange', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='event.new')
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='event.update')
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='event.delete')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=new_queue_name, on_message_callback=get_message)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)