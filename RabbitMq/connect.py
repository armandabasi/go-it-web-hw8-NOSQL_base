import pika

import pathlib
from mongoengine import connect
import configparser

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get('DEV_DB', 'USER')
mongodb_pass = config.get('DEV_DB', 'PASSWORD')
db_name = config.get('DEV_DB', 'DB_NAME')
domain = config.get('DEV_DB', 'DOMAIN')

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


def rabbit_connect():
    rabbitmq_user = config.get('RABBIT_DB', 'USER')
    rabbitmq_pass = config.get('RABBIT_DB', 'PASSWORD')
    rabbitmq_host = config.get('RABBIT_DB', 'HOST')
    rabbitmq_port = config.get('RABBIT_DB', 'PORT')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    return connection, channel
