import pika, sys

def publish_message(message,route):
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('OrganizerMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange baru yang nantinya akan dihubungkan ke satu/lebih queue oleh consumer(s)
    channel.exchange_declare(exchange='OrganizerEX', exchange_type='topic')
    # channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='event.new')
    # channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='event.update')
    # channel.queue_bind(exchange='OrganizerEX', queue=new_queue_name, routing_key='event.delete')

    # Kirimkan message ke RabbitMQ
    channel.basic_publish(exchange='OrganizerEX',
                          routing_key=route, 
                          body=message, 
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE) )

    print("Sent a message: " + message)

    connection.close()