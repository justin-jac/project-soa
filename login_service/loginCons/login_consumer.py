import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="LoginSQL", user="root", password="root",database="loginservice")
cursor = db.cursor(dictionary=True)


def main():
    db = mysql.connector.connect(host="LoginSQL", user="root", password="root",database="loginservice")
    cursor = db.cursor(dictionary=True)
    def get_message(ch, method, properties, body):

        data = json.loads(body)
        event = data['event']
        id_user = data['id']
        username = data['username']
        password = data['password']
        user_status = data['user_status']

        if (event == "client.new" or event == "staff.new"):
            sql = "INSERT INTO users VALUES(%s,%s,%s,%s)"
            cursor.execute(sql,[id_user,username,password,user_status])
            db.commit()
            message = "Sukses Menambah Data " + username
        elif (event == "client.update" or event == "staff.update"):
            sql = "UPDATE users set username=%s, password=%s WHERE id_user=%s AND user_status=%s"
            cursor.execute(sql, [username,password,id_user,user_status] )
            db.commit()
            message = "Sukses Update Data " + username
        elif (event == "client.delete" or event == "staff.delete"):
            sql = "DELETE FROM users WHERE id_user = %s AND user_status = %s"
            cursor.execute(sql, [id_user, user_status] )
            db.commit()

        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)


    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('OrganizerMQ',5672,'/',credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='OrganizerEX', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='client.*')
    channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='staff.*')

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