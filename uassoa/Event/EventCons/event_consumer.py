import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="EventSQL", user="root", password="root",database="eventdb")
dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):
        data = json.loads(body)
        event = data['event']
        message = "Tidak Merubah Database"

        if event == "order.delete":
            del_idOrder = data["idOrder"]

            # DELETE events
            sql = "DELETE FROM events WHERE idOrder=%s"
            dbc.execute(sql, [del_idOrder])
            db.commit()

            message = "Sukses Menghapus semua Event dengan idOrder "+str(del_idOrder)

        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EoMQ', 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='eoExchange', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='order.delete')

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