import pika
from connect import get_mongo_client
from contact import Contact


def callback(ch, method, properties, body):
    print("Received message:", body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages():
    mongo_client = get_mongo_client()

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='contact_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='contact_queue', on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted by user. Closing connection...')
        connection.close()


if __name__ == '__main__':
    consume_messages()
