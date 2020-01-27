from flask import Flask, escape, request, Response
import json
from BasicDB import Mongolo_ModelChunk, debug_rebuildChunks, debug_rebuildData


def initDataAPI(app, mongoloClient):

	def getData():
		try:
			data =  json.loads(request.values["data"])
		except Exception as e:
			print(e)
			return "`data` was expected", 400
		return data, None


	def debug_rebuild(data:dict):
		radius = data["radius"]
		debug_rebuildData()
		debug_rebuildChunks(radius)
		return "ok", 200


	def listTypeBlocks(data:dict):
		chunks = data["chunks"]
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
		print(bufferData)
		finalData = {}
		for name in bufferData.keys():
			finalData[mongoloClient.blockdata.getBlocks(id=name)[0]["fullname"]] = bufferData[name]
		return finalData, 200


	def identidy(data:dict):
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


	def getRef(data:dict):
		a = list(mongoloClient.blockdata.find(data["filter"]))
		for b in a:
			b["id"] = str(b["_id"])
			del b["_id"]
		return {"ref":a}, 200


	def insertChunk(data:dict):
		world = data["dim"]
		chunk = data["chunk"]
		data_ = data["data"]
		chunk = mongoloClient.Chunk(chunk["x"], chunk["y"], chunk["z"], mongoloClient.client)
		if len(data_) != 4096:
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






	@app.route("/debug/rebuild", methods=["GET", "POST"])
	def url_debug_rebuild():
		data, err = getData()
		if not err:
			return debug_rebuild(data)
		return data, err


	@app.route("/listeTypeBlocks", methods=["GET", "POST"])
	def url_listTypeBlocks():
		data, err = getData()
		if not err:
			return listTypeBlocks(data)
		return data, err


	@app.route("/identify")
	def url_identidy():
		data, err = getData()
		if not err:
			return identidy(data)
		return data, err


	@app.route("/getRef", methods=["POST", "GET"])
	def url_getRef():
		data, err = getData()
		if not err:
			return getRef(data)
		return data, err
		
	
	@app.route("/insertChunk", methods=["POST"])
	def url_insertChunk():
		data, err = getData()
		if not err:
			return insertChunk(data)
		return data, err