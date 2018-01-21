
#bitalino device simulator, simulates EMG sensor data that is sent to server which is forwarded to client.js for assessment
import sys
from twisted.internet import reactor
import random
from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS


class BroadcastClientProtocol(WebSocketClientProtocol):

    """
    Simple client that connects to a WebSocket server, send a HELLO
    message every 2 seconds and print everything it receives.
    """

    def sendHello(self):
        rand_int=random.randint(1,101)
        print("sending {}\n".format(rand_int))
        str_int=str(rand_int)
        self.sendMessage(str_int.encode('utf8'))
        reactor.callLater(5, self.sendHello)

    def onOpen(self):
        self.sendHello()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Need the WebSocket server address, i.e. ws://127.0.0.1:9000")
        sys.exit(1)

    factory = WebSocketClientFactory(sys.argv[1])
    factory.protocol = BroadcastClientProtocol
    connectWS(factory)

    reactor.run()