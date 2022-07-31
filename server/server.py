#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import random
import time
import json

from classes.SingletonNameGenerator import SingletonNameGenerator

# Configuration
random.seed()
if os.path.isfile('config.json'):
    with open('config.json') as iFile:
        data = json.load(iFile)
        database = data["options"]["base"]["name"]
        ngram = data["options"]["base"]["ngram"]
else:
    raise "Initialization: Configuration file not found"

# Load database
print("Set database: " + database)
print("Set n-gram: " + str(ngram))
t0 = time.time()
print("Load learning...")
SingletonNameGenerator.init(database, ngram)
print("Done in {0}s.".format(round(time.time() - t0, 3)))

# Init server
app = Flask(__name__)
CORS(app)


@app.route("/v1/generate", methods=['GET'])
# Generate new word
def api_v1_generate():
    # If request is GET
    if request.method == 'GET':
        # Get new word
        resp = jsonify(SingletonNameGenerator.generate())
        # OK
        resp.status_code = 200

    return resp


@app.route("/v1/ngram", methods=['GET', 'PUT'])
# Get or update n-gram
def api_v1_ngram():
    # If request is GET
    if request.method == 'GET':
        # Return selected n-gram
        resp = jsonify(SingletonNameGenerator.getSelectedNgram())
        # OK
        resp.status_code = 200

    # If request is PUT
    elif request.method == 'PUT':
        # Get new n-gram
        ngram = int(json.dumps(request.json))
        SingletonNameGenerator.reload(ngram)
        # OK but no content
        resp = jsonify("")
        resp.status_code = 204

    return resp
