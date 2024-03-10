from pymongo.mongo_client import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('./task1/config.ini')

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
