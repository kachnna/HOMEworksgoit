from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


try:
    connect(
        host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# mongodb+srv://katarzynaczempiel:Vakarian7!@cluster0.rzxrwwx.mongodb.net/?retryWrites=true&w=majority