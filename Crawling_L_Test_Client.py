from socketIO_client import SocketIO, LoggingNamespace
import logging
import json

# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)

url_array = ["http://rpi.edu/", "https://www.androidauthority.com/", "https://www.taylorswift.com/news", "http://profootballtalk.nbcsports.com/"]

# =======================================================================================================
ip = "127.0.0.1"
port = "5000"
# =======================================================================================================

def on_connect():
    print('connection to socket established at ' + ip + ':' + port)

def on_disconnect():
    print('disconnected from socket at ' + ip + ':' + port)

def on_reconnect():
    print('reconnected to socket at ' + ip + ':' + port)

def handle_crawler_data():
    print('new data received from crawler')

def handle_new_json(data):
    print('json data received from crawler\n')
    crawled_json = json.loads(data)
    print("URL:\n" + crawled_json['url'] + '\n')
    print("OUTLINKS:\n")
    print(crawled_json['outlinks'])


# =======================================================================================================

with SocketIO(ip, port, LoggingNamespace) as socketIO:
    # socketIO.on('connected', on_connect)
    # Emit
    socketIO.emit('new links', url_array)
    # Listen
    socketIO.on('new crawler data', handle_new_json)
    # Wait
    socketIO.wait()
