import pika
import connect
from connect import rabbit_connect
from seeds import upload_contacts
from models import Users
from time import sleep

NUMBER_USERS = 10

connection, channel = rabbit_connect()
channel.exchange_declare(exchange='task_mock', exchange_type='direct')
#channel.queue_declare(queue='task_queue', durable=True)
#channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    upload_contacts(NUMBER_USERS)
    users = Users.objects()

    for user in users:
        queue_type = str(user.preferred_mode)

        channel.queue_declare(queue=queue_type, durable=True)
        channel.queue_bind(exchange='task_mock', queue=queue_type)

        message = f"Dear {user.fullname}!\nYour id: {user.id}"
        channel.basic_publish(
            exchange='task_mock',
            routing_key=str(user.preferred_mode),
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f"[x] Sent to recipient {user.id}")
    connection.close()


if __name__ == '__main__':
    main()
