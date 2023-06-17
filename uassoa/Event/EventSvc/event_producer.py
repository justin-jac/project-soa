import pika, sys

def publish_message(message,route):
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EoMQ',5672,'/',credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='eoExchange', exchange_type='topic')

    # Kirimkan message ke RabbitMQ
    channel.basic_publish(exchange='eoExchange',
                          routing_key=route,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE) )

    print("Sent a message: " + message)

    connection.close()