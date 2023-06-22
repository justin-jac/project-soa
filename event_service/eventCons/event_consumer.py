import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="EventSQL", user="root", password="root",database="event")
dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):
        data = json.loads(body)
        event = data['event']
        message = "Database Not Changed"

        if event == "order.delete":
            delete_id_order = data["id_order"]

            # DELETE events
            sql = "DELETE FROM events WHERE id_order=%s"
            dbc.execute(sql, [delete_id_order])
            db.commit()
            
            # DELETE order
            sql = "DELETE FROM event_order WHERE id=%s"
            dbc.execute(sql, [delete_id_order])
            db.commit()

            message = "Succesfully deleted event with id_order " + str(delete_id_order)
        
        if event == "order.new":
            id_order = data["id_order"]
            
            # INSERT order
            sql = "INSERT INTO `event_order`(`id`) VALUES ('%s')"
            dbc.execute(sql, [id_order])
            db.commit()
            
            message = 'Added order' + str(id_order) + ' to event DB'
            
        if event == "staff.new":
            id_staff = data["id"]
            
            # INSERT staff
            sql = "INSERT INTO `event_staff`(`id`) VALUES ('%s')"
            dbc.execute(sql, [id_staff])
            db.commit()
            
            message = 'Added staff' + str(id_order) + ' to event DB'
            
        if event == "staff.delete":
            id_staff = data["id"]
            
            # DELETE staff
            sql = "DELETE FROM `event_staff` WHERE id=%s"
            dbc.execute(sql, [id_staff])
            db.commit()
            
            message = 'Deleted staff' + str(id_order) + ' in event DB'
        

        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('OrganizerMQ', 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='OrganizerEX', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='order.*')
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='staf.*')
    
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