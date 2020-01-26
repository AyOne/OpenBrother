from flask import Flask, escape, request, Response
from BasicDB import Mongolo_ModelChunk, debug_rebuildChunks, debug_rebuildData


def initFrontAPI(app, mongoloClient):
	@app.route("/front/debug/rebuild", methods=["POST"])
	def debugRebuild():
		try:
			data =  request.values["data"]
		except Exception as e:
			return "", 400
		radius = data["radius"]
		debug_rebuildData()
		debug_rebuildChunks(radius)
		return "ok", 200




	@app.route("/front/listeTypeBlocks", methods=["GET"])
	def listTypeBlocks():
		try:
			data =  request.values["data"]
		except Exception as e:
			print(e)
			return "",  400
		chunk = data["chunk"]
		filter = data["filter"] or {}
		world = data["dim"] or "overworld"
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
			finalData[mongoloClient.blockdata.getBlocks(id=name)[0]["fullname"]] = bufferData[name]
		return finalData, 200


	@app.route("front/identify")
	def identidy():
		try:
			data =  request.values["data"]
		except Exception as e:
			print(e)
			return "",  400
		if "name" in data and "mod" in data:
			blocks = mongoloClient.blockdata.getBlocks(name="{}:{}".format(data["name"], data["mod"]))
		elif "fullname" in data:
			blocks = mongoloClient.blockdata.getBlocks(fullname=data["fullname"])
		elif "id" in data:
			blocks = mongoloClient.blockdata.getBlocks(id=data["id"])
		else:
			return "", 400

		for b in blocks:
			b["id"] = str(b["_id"])
			del b["_id"]

		if len(blocks) > 0:
			return blocks, 200
		return {}, 200