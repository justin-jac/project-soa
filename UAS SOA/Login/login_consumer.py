import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="localhost", user="root", password="",database="loginservice")
cursor = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):

        data = json.loads(body)
        print(1)
        event = data['event']
        idUser = data['idUser']
        username = data['username']
        password = data['password']
        userType = data['userType']

        if (event == "client_new" or event == "staff_new"):
            sql = "INSERT INTO usertable VALUES(%s,%s,%s,%s)"
            cursor.execute(sql,[idUser,username,password,userType])
            db.commit()
            message = "Sukses Menambah Data " + username
        elif (event == "client_update" or event == "staff_update"):
            sql = "UPDATE usertable set username=%s, password=%s WHERE idUser=%s AND userType=%s"
            cursor.execute(sql, [username,password,idUser,userType] )
            db.commit()
            message = "Sukses Update Data " + username

        logging.warning("Received: %r" % message)

        ch.basic_ack(delivery_tag=method.delivery_tag)


    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='eoExchange', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='client.new')
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='client.update')
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='staff.new')
    channel.queue_bind(exchange='eoExchange', queue=new_queue_name, routing_key='staff.update')

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