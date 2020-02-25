from BasicDB import Mongolo_ModelChunk, debug_rebuildChunks, debug_rebuildData
from APIs.DataAPI import initDataAPI
from APIs.turtleAPI import initTurtleAPI
import pymongo
import random
import time
import re
import sys
import threading
import os
from flask import Flask, escape, request, Response
from flask_cors import CORS





mongoloClient = Mongolo_ModelChunk("mongodb://localhost:27017/")
blockdata = mongoloClient.blockdata
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
	return "Hello World", 200



s = initTurtleAPI(app, mongoloClient)
initDataAPI(app, mongoloClient)
app.run(threaded=True, host="0.0.0.0", port="8190", debug=False)
s.stop()
s.join()
