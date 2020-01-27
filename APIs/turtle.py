from BasicDB import debug_rebuildChunks, debug_rebuildData
from flask import Flask, escape, request, Response
import json





def initTurtleAPI(app, mongoloClient):

	@app.route("/turtle/debug/rebuild", methods=["POST", "GET"])
	def debugRebuild_():
		try:
			data = json.loads(request.values["data"])
		except Exception as e:
			print(e)
			return "", 400

		radius = data["radius"]
		debug_rebuildData()
		debug_rebuildChunks(radius)
		return "ok", 200


	@app.route("/turtle/getRef", methods=["POST", "GET"])
	def getRef_():
		try:
			data = json.loads(request.values["data"])
		except Exception as e:
			print(e)
			return "", 400
		a = list(mongoloClient.blockdata.find(data["filter"]))
		for b in a:
			b["id"] = str(b["_id"])
			del b["_id"]
		return {"data":a}, 200


	@app.route("/turtle/listeTypeBlocks", methods=["POST", "GET"])
	def listTypeBlocks_():
		try:
			data = json.loads(request.values["data"])
			chunks = data["chunks"]
			filter = data["filter"]
			world = data["dim"]
		except Exception as e:
			print(e)
			return "", 400
		
		bufferData = {}
		for chunk in chunks:
			buffer = mongoloClient.bigFind(filter, world, chunk)
			for b in buffer.keys():
				if b in bufferData:
					bufferData[b] += buffer[b]
				else:
					bufferData[b] = buffer[b]
		finalData = {}
		for name in bufferData.keys():
			finalData[mongoloClient.blockdata.getBlocks(id=name)[0]["name"]] = bufferData[name]
		return finalData, 200



	@app.route("/turtle/insertChunk", methods=["POST"])
	def insertChunk_():
		try:
			data = json.loads(request.values["data"])
			world = data["dim"]
			chunk = data["chunk"]
			data_ = data["data"]
		except Exception as e:
			print(e)
			return "", 400

		chunk = mongoloClient.Chunk(chunk["x"], chunk["y"], chunk["z"], mongoloClient.client)
		if count(data_) != 4096:
			return "", 400
		
		for d in data_:
			block = {
				"x":d["x"],
				"y":d["y"],
				"z":d["z"],
				"name":d["name"],
				"meta":d["meta"],
			}
			chunk.data.append(block)
		mongoloClient.replaceChunk(chunk, world)
		return "ok", 200

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