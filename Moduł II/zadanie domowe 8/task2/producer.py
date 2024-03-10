import pika
import json
from faker import Faker
from connect import get_mongo_client, host_connect
from contact import Contact

host_connect()

def producer_run():

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    fake = Faker()

    for _ in range(10):
        name = fake.name()
        email = fake.email()

        contact = Contact(name=name, email=email)
        contact.save()

        message = {'contact_id': str(contact.id)}
        channel.basic_publish(
            exchange='', routing_key='contact_queue', body=json.dumps(message))

    print("[*] Contacts sent to the queue")

    connection.close()

