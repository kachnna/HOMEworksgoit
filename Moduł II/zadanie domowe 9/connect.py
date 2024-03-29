from pymongo.mongo_client import MongoClient
import configparser
from mongoengine import connect


config = configparser.ConfigParser()
config.read('./config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{db_name}.{domain}/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

host = 'mongodb://localhost:27017/mydatabase'
connect(host=host, alias='default')
