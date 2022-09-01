import json
import pika
from pika import exceptions
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol,task


@defer.inlineCallbacks
def run(connection):
    channel = yield connection.channel()
    channel.exchange_declare(exchange='exchange_1', exchange_type='topic')
    channel.queue_declare(queue='train.model', auto_delete=False, exclusive=False)
    channel.queue_bind(exchange='exchange_1',queue='train.model',routing_key='train.model')
    channel.basic_qos(prefetch_count=1)

    queue_object, consumer_tag = yield channel.basic_consume('train.model', auto_ack=False)
    l = task.LoopingCall(read, queue_object)
    l.start(0.01)


@defer.inlineCallbacks
def read(queue_object):
    ch,method,properties,body = yield queue_object.get()

    if body:
        body = json.loads(body)
        print(body)

    if properties:
        print(properties.message_id)

    yield ch.basic_ack(delivery_tag=method.delivery_tag)

def on_err(err):
    print("error handled")


parameters = pika.ConnectionParameters()
cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, parameters)
d = cc.connectTCP('localhost', 5672)
d.addErrback(on_err)
d.addCallback(lambda protocol: protocol.ready)
d.addCallback(run)
reactor.run()