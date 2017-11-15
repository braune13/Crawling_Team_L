from socketIO_client import SocketIO, LoggingNamespace
import logging

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

# =======================================================================================================
ip = "127.0.01"
port = "8000"
# =======================================================================================================

def on_connect():
    print('connection to socket established at ' + ip + ':' + port)

def on_disconnect():
    print('disconnected from socket at ' + ip + ':' + port)

def on_reconnect():
    print('reconnected to socket at ' + ip + ':' + port)

def handle_crawler_data():
    print('new data received from crawler')


# =======================================================================================================

with SocketIO(ip, port, LoggingNamespace) as socketIO:
    socketIO.on('connected', on_connect)

    # Listen
    socketIO.on('new crawler data', handle_crawler_data)

    # Emit
    socketIO.emit('my message', "poop")
