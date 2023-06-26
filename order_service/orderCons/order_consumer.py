import pika, sys, os
import mysql.connector,logging, json

db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="eventorder")
dbc = db.cursor(dictionary=True)
    
def connect():
    db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="eventorder")
    dbc = db.cursor(dictionary=True)
    return db, dbc

def main():
    def get_message(ch, method, properties, body):
        data = json.loads(body)
        event = data['event']
        message = "Database Not Changed"

        if (event == "event.new"):
            id_order = data["id_order"]
            id_event = data["id_event"]
            sub_total = int(data["sub_total"])

            # Create new event
            sql = "INSERT INTO `order_events` (`id_event`, `id_order`, `sub_total`) VALUES (%s,%s,%s)"
            dbc.execute(sql, [id_event, id_order, sub_total])
            db.commit()

            # Update orders
            sql = "UPDATE orders set total_price=(SELECT SUM(sub_total) FROM order_events WHERE id_order=%s), status='Processing' WHERE id_order=%s"
            dbc.execute(sql, [id_order])
            db.commit()

            message = "Succesfully adding Total Order "+str(id_order)
            
        elif (event == "event.update"):
            id_order = data["id_order"]
            id_event = data["id_event"]
            sub_total = int(data["sub_total"])
            
            # Update existing event
            sql = "UPDATE order_events SET sub_total = %s WHERE id_event = %s"
            dbc.execute(sql, [sub_total, id_event])
            
            # Update orders
            sql = "UPDATE orders set total_price=(SELECT SUM(sub_total) FROM order_events WHERE id_order=%s), status='Processing' WHERE id_order=%s"
            dbc.execute(sql, [id_order])
            db.commit()
            
        elif (event == "event.delete"):
            id_event = data["id_event"]
            id_order = data["id_order"]
            
            # DELETE event
            sql = "DELETE FROM order_events WHERE id_event = %s"
            dbc.execute(sql, [id_event])
            
            # Update orders
            sql = "UPDATE orders set total_price=(SELECT SUM(sub_total) FROM order_events WHERE id_order=%s) WHERE id_order=%s"
            dbc.execute(sql, [id_order])
            db.commit()

        elif (event == "client.new"):
            id_user = data['id']
            sql = "INSERT INTO client VALUES(%s)"
            dbc.execute(sql,[id_user])
            db.commit()
            message = "Sukses Menambah Data " + str(id_user)
        elif (event == "client.delete"):
            sql = "DELETE FROM client WHERE id = %s AND user_status = %s"
            dbc.execute(sql, [id_user] )
            db.commit()
            message = "Sukses Menghapus Data " + id_user
        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('OrganizerMQ', 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='OrganizerEX', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='event.*')
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='client.*')

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