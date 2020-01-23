from flask import Flask, escape, request, Response
from BasicDB import Mongolo_ModelChunk, debug_rebuildChunks, debug_rebuildData


def initFrontAPI(app, mongoloClient):
	@app.route("/front/debug/rebuild", methods=["POST"])
	def debugRebuild():
		if not request.json:
			return "request not formated as JSON", 400
		if "radius" not in  request.json:
			return "\"radius\" not specified in the body", 400
		radius = request.json["radius"]
		debug_rebuildData()
		debug_rebuildChunks(radius)
		return "ok", 200




	@app.route("/front/listeTypeBlocks")
	def listTypeBlocks():
		print(request.json)
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
			buffer = mongoloClient.bigFind({}, world, chunk)
			for b in buffer.keys():
				if b in bufferData:
					bufferData[b] += buffer[b]
				else:
					bufferData[b] = buffer[b]
		finalData = {}
		for name in bufferData.keys():
			finalData[mongoloClient.blockdata.getBlocks(id=name)[0]["name"]] = bufferData[name]
		return finalData, 200

	@app.route("/front/IDtoBLOCK")
	def id_to_block():
		if not request.json:
			return "request not formated as JSON", 400
		if "id" not in request.json:
			return "\"id\" not specified in the body", 400
		blocks = mongoloClient.blockdata.getBlocks(id=request.json["id"])
		for b in blocks:
			b["id"] = str(b["_id"])
			del b["_id"]
		if len(blocks) > 0:
			return blocks[0], 200
		return {}, 200


	@app.route("/front/BLOCKtoID")
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

		blocks = mongoloClient.blockdata.getBlocks(name=block_name)
		for b in blocks:
			b["id"] = str(b["_id"])
			del b["_id"]
		if len(blocks) > 0:
			return blocks[0], 200
		return {}, 200

