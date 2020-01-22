import pymongo
import time
import re
import random
import sys
import math
from bson.objectid import ObjectId




def debug_rebuildChunks(radius:int=3):
	mongoloClient = Mongolo_ModelChunk("mongodb://localhost:27017/")
	mongoloClient.drop("overworld")
	t = time.time()
	sys.stdout.write("\r{} chunk to be generated...".format(mongoloClient.debug.radius_countD(radius)))
	random_chunks = mongoloClient.debug.many_random(radius)
	sys.stdout.write("done ({}s)\n".format(time.time() - t))
	t = time.time()
	c = mongoloClient.replaceChunk(random_chunks, "overworld", True, radius)
	print("{} chunks ({} blocks) added to the database. in {}s".format(c, c * pow(16, 3), time.time() - t))


def debug_rebuildData():

	blockdata = Mongolo_BlockData()
	blockdata.drop()
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "air"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "stone"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "goldOre"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "coalOre"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "ironOre"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "redstoneOre"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "lapisOre"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "diamondOre"))
	blockdata.insert(Mongolo_BlockData.Data("minecraft", "emeraldOre"))





class Mongolo_BlockData():
	def __init__(self, url:str="mongodb://localhost:27017/"):
		self.db = pymongo.MongoClient(url)["BlockData"]
		self.ref = self.db["ref"]
		self.data = self.db["data"]



	class Data():
		def __init__(self, mod:str="default", block:str="default", color:str="#FF00FF"):
			self.name = "{}:{}".format(mod, block)
			self.mod = mod
			self.block = block
			self.color = color
			self.json = {
				"name": self.name,
				"mod": self.mod,
				"block": self.block,
				"color": self.color
			}

	def insert(self, data:Data):
		objid = self.data.find_and_modify({"name":data.name}, data.json)
		if not objid:
			objid = self.data.insert_one(data.json)
		return objid.inserted_id
		

	def find(self, filter):
		return list(self.data.find(filter))

	def drop(self):
		self.data.drop()
		self.ref.drop()

	def getBlocks(self, id:str=None, block:str=None, mod:str=None, name:str=None, color:str=None):
		filter = {}
		if id is not None:
			filter["_id"] = ObjectId(id)
		if block is not None:
			filter["block"] = block
		if mod is not None:
			filter["mod"] = mod
		if name is not None:
			filter["name"] = name
		if color is not None:
			filter["color"] = color
		return list(self.data.find(filter))









class Mongolo_ModelChunk():
	def __init__(self, url:str="mongodb://localhost:27017/"):
		self.client = pymongo.MongoClient(url)
		self.blockdata = Mongolo_BlockData()
		self.debug = self.Debug(self, self.blockdata)


	class Debug():
		def __init__(self, ModelChunk, blockdata):
			self.ModelChunk = ModelChunk
			self.blockdata = blockdata
			self.blocks = self.createBlockList()

		def createBlockList(self):
			blocks = []
			while True:
				try:
					blocks += [str(self.blockdata.getBlocks(name="minecraft:air")[0]["_id"])] * 10
					blocks += [str(self.blockdata.getBlocks(name="minecraft:stone")[0]["_id"])] * 10
					blocks += [str(self.blockdata.getBlocks(name="minecraft:goldOre")[0]["_id"])] * 2
					blocks += [str(self.blockdata.getBlocks(name="minecraft:coalOre")[0]["_id"])] * 5
					blocks += [str(self.blockdata.getBlocks(name="minecraft:ironOre")[0]["_id"])] * 4
					blocks += [str(self.blockdata.getBlocks(name="minecraft:redstoneOre")[0]["_id"])] * 2
					blocks += [str(self.blockdata.getBlocks(name="minecraft:lapisOre")[0]["_id"])] * 2
					blocks += [str(self.blockdata.getBlocks(name="minecraft:diamondOre")[0]["_id"])]
					blocks += [str(self.blockdata.getBlocks(name="minecraft:emeraldOre")[0]["_id"])]
					return blocks
				except IndexError as e:
					debug_rebuildData()

		def radius_count(self, radius):
			def gc_2d(radius):
				if radius <= 0:
					return 1
				return radius * 4 + gc_2d(radius - 1)
			def gc_3d(origin, index):
				if origin <= index:
					return gc_2d(index)
				return gc_2d(index) * 2 + gc_3d(origin, index + 1)
			return gc_3d(radius, 0) * 4096
		
		def radius_countD(self, radius):
			def gc_2d(radius):
				if radius <= 0:
					return 1
				return radius * 4 + gc_2d(radius - 1)
			def gc_3d(origin, index):
				if origin <= index:
					return gc_2d(index)
				return gc_2d(index) * 2 + gc_3d(origin, index + 1)
			return gc_3d(radius, 0)


		def random_block(self, name=None, x=None, y=None, z=None, meta=None):
			if name is None:
				name = random.choice(self.blocks)
			if y is None:
				y = random.randint(0, 0xFFFFFFFF)
			if x is None:
				x = random.randint(0, 0xFFFFFFFF)
			if z is None:
				z = random.randint(0, 0xFFFFFFFF)
			if meta is None:
				meta = random.randint(0, 255)
			data = {
				"name":name,
				"y":y,
				"z":z,
				"x":x,
				"meta":meta,
			}
			return data

		def random_chunk(self, x=None, y=None, z=None):
			if x is None:
				x = random.randint(0, 0xFFFFFFFF)
			if y is None:
				y = random.randint(0, 0xFFFFFFFF)
			if z is None:
				z = random.randint(0, 0xFFFFFFFF)
			chunk = self.ModelChunk.Chunk(x, y, z, self.ModelChunk.client)
			for x_ in range(16):
				for y_ in range(16):
					for z_ in range(16):
						chunk.data.append(self.random_block(x=x_, y=y_, z=z_))
			return chunk

		def many_random(self, radius:int):
			count = 0
			finalData = []
			for x in range(-radius, radius + 1):
				for z in range(-(radius - abs(x)), (radius + 1) - abs(x)):
					for y in range(-(radius - (abs(x) + abs(z))), (radius + 1) - (abs(x) + abs(z))):
						finalData.append(self.random_chunk(x, y, z))
			return finalData

	class Chunk():
		def __str__(self):
			return "%d-%d-%d" % (self.x, self.y, self.z)

		def __init__(self, x:int, y:int, z:int, client:pymongo.database.Database):
			self.x = x
			self.y = y
			self.z = z
			self.client = client
			self.db = None
			self.data = []

		def initData(self):
			if not self.db:
				raise Exception("not connected")
			self.data = list(self.db.find({}))
		def connect(self, world:str):
			if not self.db:
				self.db = self.client[world][str(self)]


	def getChunkFromBlock(self, block:dict, world:str):
		db = self.client[world]
		chunk = {
			"x":math.floor(block["x"] / 16),
			"y":math.floor(block["y"] / 16),
			"z":math.floor(block["z"] / 16),
			"data":None
		}
		if Rdb:	#return db ?
			chunk["chunk"] = db["%d-%d-%d" % (chunk["x"], chunk["y"], chunk["z"])]
		return chunk

	def getChunk(self, x:int, y:int, z:int, world:str):
		chunk = {
			"x":math.floor(block["x"] / 16),
			"y":math.floor(block["y"] / 16),
			"z":math.floor(block["z"] / 16),
			"chunk": world["%d-%d-%d" % (chunk["x"], chunk["y"], chunk["z"])]
		}
		return chunk


	def isInChunk(self, block:dict, chunk:dict):
		if math.floor(block["x"] / 16) != chunk["x"]:
			return False
		elif math.floor(block["y"] / 16) != chunk["y"]:
			return False
		elif math.floor(block["z"] / 16) != chunk["z"]:
			return False
		return True

	def replaceChunk(self, chunks:[Chunk, list], world:str, debug=False, radius=0):
		len = self.debug.radius_countD(radius)
		counter = 0
		b = 0
		if debug:
			sys.stdout.write("\rfill progress : 0%")


		if type(chunks) == list:
			for chunk in chunks:
				if not (chunk.y >= 0 and chunk.y <= 15):
					continue
				chunk.connect(world)
				chunk.db.drop()
				chunk.db.insert_many(chunk.data)

				if debug:
					counter += 1
					p = (counter / len) * 100
					if b + 1 < p:
						b = int(p)
						sys.stdout.write("\rfill progress : {}%".format(b))
		else:
			chunks.connect(world)
			chunks.db.drop()
			chunks.db.insert_many(chunks.data)

		if debug:
			sys.stdout.write("\rfill progress : 100%\n")
		return counter

	def drop(self, world:str):
		db = self.client[world]
		for name in db.list_collection_names():
			db.drop_collection(name)


	def bigFind(self, filter:dict, world:str, chunk:dict):
		db = self.client[world]
		finalData = {}


		if not "x" in chunk:
			chunk["x"] = ".*"
		if not "y" in chunk:
			chunk["y"] = ".*"
		if not "z" in chunk:
			chunk["z"] = ".*"



		regex = "^{}-{}-{}$".format(chunk["x"], chunk["y"], chunk["z"])


		for name in db.collection_names():
			match = re.match(regex, name)
			if match:
				chunk = db[name]
				data = list(chunk.find(filter))
				for block in data:
					if block["name"] in finalData:
						finalData[block["name"]] += 1
					else:
						finalData[block["name"]] = 1
		return finalData



	def find(self, filter:dict, world:str, chunk:Chunk):
		chunk.connect()
		return chunk.db.find(filter)