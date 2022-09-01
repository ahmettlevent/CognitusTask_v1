import json
import pika
from pika import spec
from pika.adapters import twisted_connection
from pika.exchange_type import ExchangeType
from twisted.internet import reactor, protocol, defer
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

PREFETCH_COUNT = 2
EXCHANGE = "exchange_1"
ROUTING_KEY = "train.model"

class PikaProtocol(twisted_connection.TwistedProtocolConnection):
    connected = False
    name = "AMQP:Protocol"

    def __init__(self, factory, parameters):
        super().__init__(parameters)
        self.factory = factory

    @inlineCallbacks
    def connectionReady(self):
        self._channel = yield self.channel()
        yield self._channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        self.connected = True
        yield self._channel.confirm_delivery()
        for (
                exchange,
                routing_key,
                callback,
        ) in self.factory.read_list:
            yield self.setup_read(exchange, routing_key, callback)

        self.send()

    @inlineCallbacks
    def read(self, exchange, routing_key, callback):
        """Add an exchange to the list of exchanges to read from."""
        if self.connected:
            yield self.setup_read(exchange, routing_key, callback)

    @inlineCallbacks
    def setup_read(self, exchange, routing_key, callback):
        """This function does the work to read from an exchange."""
        if exchange:
            yield self._channel.exchange_declare(
                exchange=exchange,
                exchange_type=ExchangeType.topic,
                durable=False,
                auto_delete=False,
            )

        yield self._channel.queue_declare(queue=routing_key, durable=False)
        if exchange:
            yield self._channel.queue_bind(queue=routing_key, exchange=exchange)
            yield self._channel.queue_bind(
                queue=routing_key, exchange=exchange, routing_key=routing_key
            )

        (
            queue,
            _consumer_tag,
        ) = yield self._channel.basic_consume(queue=routing_key, auto_ack=False)
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)

    def _read_item(self, item, queue, callback):
        """Callback function which is called when an item is read."""
        d = queue.get()
        d.addCallback(self._read_item, queue, callback)
        d.addErrback(self._read_item_err)
        (
            channel,
            deliver,
            _props,
            msg,
        ) = item

        log.msg(
            "%s (%s): %s" % (deliver.exchange, deliver.routing_key, repr(msg)),
            system="Pika:<=",
        )
        d = defer.maybeDeferred(callback, item)
        d.addCallbacks(
            lambda _: channel.basic_ack(deliver.delivery_tag),
            lambda _: channel.basic_nack(deliver.delivery_tag),
        )

    @staticmethod
    def _read_item_err(error):
        print(error)

    def send(self):
        """If connected, send all waiting messages."""
        if self.connected:
            while self.factory.queued_messages:
                (
                    exchange,
                    r_key,
                    message,
                ) = self.factory.queued_messages.pop(0)
                self.send_message(exchange, r_key, message)

    @inlineCallbacks
    def send_message(self, exchange, routing_key, msg):
        """Send a single message."""
        log.msg("%s (%s): %s" % (exchange, routing_key, repr(msg)), system="Pika:=>")
        yield self._channel.exchange_declare(
            exchange=exchange,
            exchange_type=ExchangeType.topic,
            durable=False,
            auto_delete=False,
        )
        prop = spec.BasicProperties(delivery_mode=2)
        try:
            yield self._channel.basic_publish(
                exchange=exchange, routing_key=routing_key, body=msg, properties=prop
            )
        except Exception as error:  # pylint: disable=W0703
            log.msg("Error while sending message: %s" % error, system=self.name)


class PikaFactory(protocol.ReconnectingClientFactory):
    name = "AMQP:Factory"

    def __init__(self, parameters):
        self.parameters = parameters
        self.client = None
        self.queued_messages = []
        self.read_list = []

    def startedConnecting(self, connector):
        log.msg("Started to connect.", system=self.name)

    def buildProtocol(self, addr):
        self.resetDelay()
        log.msg("Connected", system=self.name)
        self.client = PikaProtocol(self, self.parameters)
        return self.client

    def clientConnectionLost(self, connector, reason):  # pylint: disable=W0221
        log.msg("Lost connection.  Reason: %s" % reason.value, system=self.name)
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        log.msg("Connection failed. Reason: %s" % reason.value, system=self.name)
        protocol.ReconnectingClientFactory.clientConnectionFailed(
            self, connector, reason
        )

    def send_message(self, exchange=None, routing_key=None, message=None):
        self.queued_messages.append((exchange, routing_key, message))
        if self.client is not None:
            self.client.send()

    def read_messages(self, exchange, routing_key, callback):
        """Configure an exchange to be read from."""
        self.read_list.append((exchange, routing_key, callback))
        if self.client is not None:
            self.client.read(exchange, routing_key, callback)



def main():
    parameters = pika.ConnectionParameters(
        host="localhost",
        virtual_host="/",
        credentials=pika.PlainCredentials("guest", "guest"),
    )

    def callback(ch):
        body = json.loads(ch[-1])
        properties = ch[2]
        print(properties.message_id)
        print(body)

    f = PikaFactory(parameters)
    f.read_messages(EXCHANGE, ROUTING_KEY, callback)

    reactor.connectTCP(parameters._host, parameters._port, f)

    reactor.run()
    

if __name__ == "__main__":
    main()