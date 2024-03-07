from mongoengine import connect

host = 'mongodb://localhost:27017/mydatabase'

connect(host=host, alias='default')
