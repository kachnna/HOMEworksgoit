import pika
from connect import get_mongo_client, host_connect
from contact import Contact
import json

host_connect()


def send_email(contact_id):
    print(f"Sent email to contact with ID: {contact_id}")


def callback(ch, method, properties, body):
    print("\n[x] Received message:", body)
    contact_id = json.loads(body)['contact_id']
    contact = Contact.objects.get(id=contact_id)
    send_email(contact.email)
    contact = Contact.objects.get(id=contact_id)
    contact.email_sent = True
    contact.save()

    print(f"Marked contact with ID {contact_id} as email sent.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages():

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
