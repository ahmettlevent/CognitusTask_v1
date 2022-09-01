import pika
import json
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange="exchange_1",
    exchange_type="topic",
    )


train_preferences = {
    "data_url": "https://miro.medium.com/max/724/1*JKhDtrILrWho1U-TEOzmYA.png",
    "result_backend_uri" : "localhost",
}

channel.basic_publish(
    exchange="exchange_1",
    routing_key="train.model",
    properties=pika.BasicProperties(message_id=str(uuid.uuid4())),
    body=json.dumps(train_preferences)
)

connection.close()