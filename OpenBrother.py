from BasicDB import Mongolo_ModelChunk, debug_rebuildChunks, debug_rebuildData
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



@app.route("/IDtoBLOCK")
def id_to_block():
	if not request.json:
		return "request not formated as JSON", 400
	if "id" not in request.json:
		return "\"id\" not specified in the body", 400
	blocks = blockdata.getBlocks(id=request.json["id"])
	for b in blocks:
		b["id"] = str(b["_id"])
		del b["_id"]
	if len(blocks) > 0:
		return blocks[0], 200
	return {}, 200

@app.route("/BLOCKtoID")
def block_to_id():
	if not request.json:
		return "request not formated as JSON", 400
	if "data" not in request.json:
		return "\"data\" not specified in the body", 400

	block_name = None
	if "name" in request.json["data"]:
		block_name = request.json["data"]["name"]
	elif "block" in request.json["data"] and "mod" in request.json["data"]:
		block_name = "{}:{}".format(request.json["data"]["mod"], request.json["data"]["block"])
	else:
		return "data not formated as intented", 400

	blocks = blockdata.getBlocks(name=block_name)
	for b in blocks:
		b["id"] = str(b["_id"])
		del b["_id"]
	if len(blocks) > 0:
		return blocks[0], 200
	return {}, 200

@app.route("/listeTypeBlocks")
def listTypeBlocks():
	if not request.json:
		return "request not formated as JSON", 400
	if "chunks" not in request.json:
		return "\"chunk\" not specified in the body", 400
	chunks = request.json["chunks"]
	if "filter" not in request.json:
		return "\"filter\" not specified in the body", 400
	filter = request.json["filter"]
	if "dim" not in  request.json:
		return "\"dim\" not speficied in the body", 400
	world = request.json["dim"]
	bufferData = {}
	for chunk in chunks:
		buffer = mongoloClient.bigFind({}, "overworld", chunk)
		for b in buffer.keys():
			if b in bufferData:
				bufferData[b] += buffer[b]
			else:
				bufferData[b] = buffer[b]
	finalData = {}
	for name in bufferData.keys():
		finalData[blockdata.getBlocks(id=name)[0]["name"]] = bufferData[name]
	return finalData, 200


@app.route("/debug/rebuild", methods=["POST"])
def debugRebuild():
	if not request.json:
		return "request not formated as JSON", 400
	if "radius" not in  request.json:
		return "\"radius\" not specified in the body", 400
	radius = request.json["radius"]
	debug_rebuildData()
	debug_rebuildChunks(radius)
	return "ok", 200


#testing(3)



app.run(threaded=True, host="0.0.0.0", port="8190", debug=True)

