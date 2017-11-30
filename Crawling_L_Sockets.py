import socketio
import eventlet
from flask import Flask, render_template
from Crawling_L import get_webpages, parse_webpages

sio = socketio.Server()
app = Flask(__name__)

# -------------------------------------------------------------------------------------------------------
# Just loads a shitty index page if the user goes to ip:port in a web browser

@app.route('/')
def index():
    # Serve the client-side application
    return render_template('index.html')

# -------------------------------------------------------------------------------------------------------
# Listens for a client member connecting, prints connection info to console

@sio.on('connect')
def connect(sid, environ):
    print('connect ' + sid)

# -------------------------------------------------------------------------------------------------------
# Listens for a client member disconnecting, prints disconnection info to console

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

# -------------------------------------------------------------------------------------------------------
# Listens for 'new links' message where data is a list of links

@sio.on('new links')
def message(sid, data):
    print('New links array: ', data)
    # this is where the the parallel function that Aidan is making should be called, taking in data
    output = parse_webpages(data)
    send_crawled_json(output)

# -------------------------------------------------------------------------------------------------------
# Emits JSON object to all clients connected to the socket server

def send_crawled_json(json_data):
    print('sending the json data')
    sio.emit('new crawler data', json_data)

# -------------------------------------------------------------------------------------------------------
# Main

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
