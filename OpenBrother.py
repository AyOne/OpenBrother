import socket
from BasicDB import Mongolo_ModelX, Mongolo_ModelChunk, testing
from inputs import get_gamepad
import threading
import asyncio
import pymongo
import random
import time
import re
import sys
from flask import Flask, escape, request


mongoloClient = Mongolo_ModelChunk("mongodb://localhost:27017/")
app = Flask(__name__)


@app.route("/")
def hello():
	return "Hello World"


@app.route("/ModelX/getBlockAt/<int:x>/<int:y>/<int:z>", methods=["GET"])
def getBlockAt(x=None,y=None,z=None):
	filter = {}
	if x is not None:
		filter["x"] = x
	if y is not None:
		filter["y"] = y
	if z is not None:
		filter["z"] = z
	r = mongoloClient.find(filter, "overworld", False)
	print(r)
	print(len(r))
	try:
		return r[0]
	except Exception as e:
		print(e)
		return r

@app.route("/ModelX/setBlockAt/<int:x>/<int:y>/<int:z>/<int:meta>/<string:name>", methods=["POST"])
def setBlockAt(x, y, z, meta, name):
	block = {"x":x, "y":y, "z":z, "meta":meta, "name":name}
	print(block)
	mongoloClient.findNreplace(block, {"x":x, "y":y, "z":z}, "overworld")
	return "Ok"






testing(3)



#app.run(threaded=True)

