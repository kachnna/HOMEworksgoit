import pika
import json
from faker import Faker
from connect import get_mongo_client
from contact import Contact
from mongoengine import connect

host = 'mongodb://localhost:27017/mydatabase'
connect(host=host, alias='default')


def producer_run():
    mongo_client = get_mongo_client()

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

        message = {'contact_id': str(contact.id), 'name': str(name), 'email':str(email)}
        channel.basic_publish(
            exchange='', routing_key='contact_queue', body=json.dumps(message))

    print("Contacts sent to the queue")

    connection.close()


if __name__ == "__main__":
    producer_run()
