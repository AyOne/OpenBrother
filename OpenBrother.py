from BasicDB import Mongolo_ModelChunk, debug_rebuildChunks, debug_rebuildData
from APIs.turtle import initTurtleAPI
from APIs.front import initFrontAPI
import pymongo
import random
import time
import re
import sys
from flask import Flask, escape, request, Response
from flask_cors import CORS


mongoloClient = Mongolo_ModelChunk("mongodb://localhost:27017/")
blockdata = mongoloClient.blockdata
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
	return "Hello World", 200





#testing(3)


initFrontAPI(app, mongoloClient)
initTurtleAPI(app, mongoloClient)
app.run(threaded=True, host="0.0.0.0", port="8190", debug=True)

