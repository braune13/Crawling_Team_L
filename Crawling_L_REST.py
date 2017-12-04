# Imports

from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
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


# ==================================================================================
# MAIN

if __name__ == '__main__':
    app.run(debug=True)
