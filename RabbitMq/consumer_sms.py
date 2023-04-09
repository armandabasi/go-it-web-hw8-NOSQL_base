import sys

import pika
from time import sleep
from connect import rabbit_connect
from models import Users

connection, channel = rabbit_connect()

TYPE_CONSUMER = "sms"

channel.queue_declare(queue=TYPE_CONSUMER, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_sms(message):
    users = Users.objects()
    for user in users:
        if message.split(":")[1].strip() == str(user.id):
            sleep(1)
            print(f"Sms has been sent to user {user.fullname}")


def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received \n{message}")
    send_sms(message)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=TYPE_CONSUMER, on_message_callback=callback)

if __name__ == '__main__':
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted! Bye!")
        sys.exit(0)
