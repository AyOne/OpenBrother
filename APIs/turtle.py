from BasicDB import debug_rebuildChunks, debug_rebuildData
from flask import Flask, escape, request, Response
import json





def initTurtleAPI(app, mongoloClient):

	@app.route("/turtle/debug/rebuild", methods=["POST", "GET"])
	def debugRebuild_():
		try:
			radius = int(request.values["radius"])
		except Exception as e:
			return "\"radius\" not specified in the data", 400
		debug_rebuildData()
		debug_rebuildChunks(radius)
		return "ok", 200




	@app.route("/turtle/listeTypeBlocks", methods=["POST", "GET"])
	def listTypeBlocks_():
		try:
			chunks = json.loads(request.values["chunks"])
			filter = json.loads(request.values["filter"])
			world = request.values["dim"]
		except Exception as e:
			print(e)
			return "one of the following isn't speficied in the data : \"chunks\" | \"filter\" | \"dim\"", 400
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



	@app.route("/turtle/insertChunk", methods=["POST"])
	def insertChunk_():
		try:
			world:str = request.values["dim"]
			data:str = request.values["data"]
		except Exception as e:
			print(e)
			return "one of the following isn't speficied in the data : \"data\" | \"dim\"", 400
		coords, data = data.split("<", 1)
		Cx, Cy, Cz = [int(c) for c in coords.split(" ", 2)]
		data = data[0:-1]
		data = data.split("|")
		chunk = mongoloClient.Chunk(Cx, Cy, Cz, mongoloClient.client)
		for d in data:
			d = d.split(" ", 4)
			block = {
				"x":int(d[0]),
				"y":int(d[1]),
				"z":int(d[2]),
				"name":d[3],
				"meta":int(d[4]),
			}
			chunk.data.append(block)
		mongoloClient.replaceChunk(chunk, world)
		return "ok", 200

