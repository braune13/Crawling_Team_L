# Imports

from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json
import requests
import Crawling_L_Threading
import Crawling_L
# ==================================================================================
# Configuration

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://admin:password1234@ds125896.mlab.com:25896/crawling_team_l'

mongo = PyMongo(app)

# ==================================================================================
# ROUTES
# ----------------------------------------------------------------------------------
# Loads an index page that just tells the user to use our API ROUTES


@app.route('/')
def index():
    # Serve the client-side application
    return render_template('index.html')
# ----------------------------------------------------------------------------------
# Takes a list of url strings and calls the crawler, passing it the URLs


@app.route('/new_links', methods=['POST'])
def new_links():
    # Get links list out of post request
    links = request.json['links']

    # Loop through links array add each link to the queue
    for link in links:
        thread_manager.addToQueue(link)

    # Return success message
    output = {
        'status': 'success',
        'message': 'Links successfully added'
    }
    return jsonify({'result': output})
# ----------------------------------------------------------------------------------
# Takes a json object from a crawled webpage and adds it to the mongo database

# @app.route('/add_webpage', methods=['POST'])


def add_webpage(url_data):
    webpages = mongo.db.webpages
    # url_json = json.loads(url_data)
    url = url_data['url']

    is_found = webpages.find_one({'url': url})
    if is_found:
        webpages.delete_one({'url': url})

    webpage_id = webpages.insert_one(url_data)

    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    r = requests.post("http://teamz.cs.rpi.edu:8080/document",
                      data=dumps(url_data), headers=headers)

    id_string = str(webpage_id)

    output = {
        'status': 'success',
        'message': 'Webpage data successfully added to mongo',
        'id': id_string
    }

    return {'result': output}
# ==================================================================================
# MAIN


if __name__ == '__main__':
    # creates threadmanager and spawns threads
    thread_manager = Crawling_L_Threading.threadManager()
    app.run(host='0.0.0.0', port=8080, debug=True)
