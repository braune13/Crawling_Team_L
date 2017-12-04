# Imports

from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from Crawling_L_Threading import threadManager
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
    output = {'status': 'success', 'message': 'Links successfully added to queue'}
    return jsonify({'result' : output})
# ==================================================================================
# MAIN

if __name__ == '__main__':
    thread_manager = threadManager()
    app.run(debug=True)
