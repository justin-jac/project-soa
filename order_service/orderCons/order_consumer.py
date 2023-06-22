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

        if event == "event.new":
            new_id_event = data["id_event"]
            id_order = data["id_order"]
            sub_total = data["sub_total"]

            # Add events
            sql = "INSERT INTO orders_events (id_event, id_order, sub_total) VALUES (%s,%s,%s)"
            dbc.execute(sql, [new_id_event, id_order, sub_total])
            db.commit()

            # Update orders
            sql = "SELECT total_price FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id_order])
            prev_total = dbc.fetchone()['total_price']
            new_total_order = prev_total + sub_total

            sql = "UPDATE orders SET total_price=%s WHERE id_order=%s"
            dbc.execute(sql, [new_total_order, id_order])
            db.commit()

            message = "Succesfully adding Total Order "+str(id_order)+" & Event "+str(new_id_event)

        elif event == "event.update":
            id_event = data["id_event"]
            id_order = data["id_order"]
            new_sub_total = data["sub_total"]

            # Get previous sub_total
            sql = "SELECT sub_total FROM order_events WHERE id_event=%s"
            dbc.execute(sql, [id_event])
            prev_sub_total = dbc.fetchone()["sub_total"]

            selisih_sub_total = new_sub_total - prev_sub_total

            # Update events
            sql = "UPDATE order_events SET sub_total=%s WHERE id_event=%s"
            dbc.execute(sql, [new_sub_total, id_event])
            # dbc.execute(sql, [selisih_sub_total, id_event])
            db.commit()

            # Update orders
            sql = "SELECT total_price FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id_order])
            prev_total = dbc.fetchone()['total_price']
            new_total_order = prev_total + selisih_sub_total

            sql = "UPDATE orders SET total_price=%s WHERE id_order=%s"
            dbc.execute(sql, [new_total_order, id_order])
            db.commit()

            message = "Succesfully changing Total Order "+str(id_order)+" & Event "+str(id_event)

        elif event == "event.delete":
            del_id_event = data["id_event"]

            # Get id_order & sub_total
            sql = "SELECT id_order, sub_total FROM order_events WHERE id_event=%s"
            dbc.execute(sql, [del_id_event])
            data_del = dbc.fetchone()
            id_order = data_del["id_order"]
            del_sub_total = data_del["sub_total"]

            # DELETE events
            sql = "DELETE FROM order_events WHERE id_event=%s"
            dbc.execute(sql, [del_id_event])
            db.commit()

            # Update orders
            sql = "SELECT total_price FROM orders WHERE id_order = %s"
            dbc.execute(sql, [id_order])
            prev_total = dbc.fetchone()['total_price']
            new_total_order = prev_total - del_sub_total

            sql = "UPDATE orders SET total_price=%s WHERE id_order=%s"
            dbc.execute(sql, [new_total_order, id_order])
            db.commit()

            message = "Succesfully Reducing Total Order "+str(id_order)+" & Deleting Event "+str(del_id_event)

        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('OrganizerMQ', 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='OrganizerEX', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='order.new')
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='order.update')
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='order.delete')

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