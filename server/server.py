#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import sys
import time
import json

from classes.SingletonNameGen import SingletonNameGen

# Params
ngram = 4
database = "ville.out"

random.seed()
hasParam = len(sys.argv) > 0

if hasParam and "-ngram" in sys.argv:
    i = sys.argv.index("-ngram")
    if len(sys.argv) > i+1:
        # Load namegenerator data
        n = int(sys.argv[i+1])
        print("Set ngram: " + str(n))
        ngram = n
    else:
        print("Error, need number of ngram")
        exit(1)

t0 = time.time()
# Load learning from file
if hasParam and "-load" in sys.argv:
    i = sys.argv.index("-load")
    if len(sys.argv) > i+1:
        # Load namegenerator data
        fn = sys.argv[i+1]
        print("Loading: " + fn)
        SingletonNameGen.initFromNgram(fn)
    else:
        print("Error, need filename to load")
        exit(1)
else:
    # No params, learn from default database
    print("Learning.")
    SingletonNameGen.initFromDatabase(ngram, database)

t1 = time.time()

print("Done in {0}s.".format(round(t1-t0, 3)))

if hasParam and "-gen" in sys.argv:
    i = sys.argv.index("-gen")
    if len(sys.argv) > i+1:
        print("-------------")
        nGen = int(sys.argv[i+1])
        for i in range(nGen):
            print(SingletonNameGen.gen())
        print("-------------")
    else:
        print("Warning, need parameter to generate names")

# Save to file after
if hasParam and "-save" in sys.argv:
    i = sys.argv.index("-save")
    if len(sys.argv) > i+1:
        fn = sys.argv[i+1]
        SingletonNameGen.nameGenerator.saveToFile(fn)
    else:
        print("Warning, need filename to save, learning not saved")

app = Flask(__name__)
CORS(app)


@app.route("/generate", methods=['GET'])
def generate():
    if request.method == 'GET':
        resp = jsonify(SingletonNameGen.gen())
        resp.status_code = 200

    return resp


@app.route("/ngram", methods=['GET', 'PUT'])
def nGram():
    global ngram

    if request.method == 'GET':
        resp = jsonify(ngram)
        resp.status_code = 200

    elif request.method == 'PUT':
        ngram = json.dumps(request.json)
        resp = jsonify("")
        resp.status_code = 204
    
    return resp
