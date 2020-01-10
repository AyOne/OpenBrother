import pymongo
import time
import re
import random
import unittest
import sys
import math



def testing(r):
	mongoloClient = Mongolo_ModelChunk("mongodb://localhost:27017/")
	mongoloClient.drop("overworld")
	t = time.time()
	sys.stdout.write("\r{} chunk to be generated...".format(mongoloClient.debug.radius_countD(r)))
	random_chunks = mongoloClient.debug.many_random(r)
	sys.stdout.write("done ({}s)\n".format(time.time() - t))
	t = time.time()
	c = mongoloClient.replaceChunk(random_chunks, "overworld", True, r)
	print("{} chunks ({} blocks) added to the database. in {}s".format(c, c * pow(16, 3), time.time() - t))



blocks = ["minecraft:air", "minecraft:ore"]

class Mongolo_ModelX(): #useless.
	def __init__(self, url:str="mongodb://localhost:27017/"):
		self.client = pymongo.MongoClient(url)
		self.debug = self.Debug(self)



	class Debug():
		def __init__(self, ModelX):
			self.ModelX = ModelX


		blocks = [
			"minecraft:air",
			"minecraft:ore"
		]

		def random_block(self, name=None, x=None, y=None, z=None, meta=None):
			if name is None:
				name = random.choice(blocks)
			if y is None:
				y = random.randint(0, 0xFFFFFFFF)
			if x is None:
				x = random.randint(0, 0xFFFFFFFF)
			if z is None:
				z = random.randint(0, 0xFFFFFFFF)
			if meta is None:
				meta = random.randint(0, 0xFFFFFFFF)
			data = {
				"name":name,
				"y":y,
				"z":z,
				"meta":meta,
			}
			return [data, x]

		def radius_count(self, radius):
			def gc_2d(radius):
				if radius == 0:
					return 1
				return radius * 4 + gc_2d(radius-1)
			def gc_3d(origin, index):
				if origin == index:
					return gc_2d(index)
				return gc_2d(index) * 2 + gc_3d(origin, index + 1)
			return gc_3d(radius, 0)

		def fill_up(self, db:[str, pymongo.database.Database, pymongo.collection.Collection], radius=16):
			len = self.radius_count(radius)
			counter = 0
			b = 0
			sys.stdout.write("\rfill progress : 0%")
			if type(db) == pymongo.collection.Collection:
				for z in range(-(radius - abs(x)), radius - abs(x)):
					for y in range(-(radius - (abs(x) + abs(z))), radius - (abs(x) + abs(z))):
						data = Mongolo_ModelX.Debug.random_block(x=x, y=y, z=z)
						ModelX.findNreplace(data, {"y":y, "z":z}, collection)
						counter += 1
						p = (counter / len) * 100
						if b + 1 < p:
							sys.stdout.write("\rfill progress : {}%".format(p))
						
						
			elif type(db) == str:
				db = self.ModelX.client[db]
				for x in range(-radius, radius + 1):
					collection = db[str(x)]
					for z in range(-(radius - abs(x)), (radius + 1) - abs(x)):
						for y in range(-(radius - (abs(x) + abs(z))), (radius + 1) - (abs(x) + abs(z))):
							data = self.random_block(x=x, y=y, z=z)[0]
							self.ModelX.findNreplace(data, {"y":y, "z":z}, collection)
							counter += 1
							p = (counter / len) * 100
							if b + 1 < p:
								b = int(p)
								sys.stdout.write("\rfill progress : {}%".format(int(p)))
			sys.stdout.write("\rfill progress : 100%\n")
			return counter



	def drop(self, db:[str, pymongo.database.Database, pymongo.collection.Collection]=None):
		if type(db) == pymongo.collection.Collection:
			db.drop()
			return
		if type(db) == str:
			db = self.client[db]
		for name in db.list_collection_names():
			db.drop_collection(name)




	def find(self, filter: dict, db:[str, pymongo.database.Database, pymongo.collection.Collection], id:bool=False):
		#if db is a collection, no need for more querrys. low cost
		if type(db) == pymongo.collection.Collection:
			return db.find(filter)
		if type(db) == str:
			db = self.client[db]
		finalData = []
		if "x" in filter:
			collection = db[str(filter["x"])]
			del filter["x"]
			print(filter)
			r = collection.find(filter)
			finalData += list(collection.find(filter))
		else:
			for name in db.list_collection_names():
				collection = db[name]
				finalData += list(collection.find(filter))
		if id is False:
			for data in finalData:
				del data["_id"]
		return finalData

	def findNreplace(self, data: dict, filter: dict, db:[str, pymongo.database.Database, pymongo.collection.Collection]):
		#if db is a collection, no need for more querrys. low cost
		if type(db) == pymongo.collection.Collection:
			if db.find_one_and_replace(filter, data) == None:
				db.insert_one(data)
			return
		#get the database object
		if type(db) == str:
			db = self.client[db]
		#if X is speficied in the filter, no need to search in all collections. low cost
		if "x" in filter:
			collection = db[str(filter["x"])]
			del filter["x"]
			if collection.find_one_and_replace(filter, data) == None:
				collection.insert_one(data)
		#else... meh. let's querry them all... warning : heavy cost
		else:
			for name in db.list_collection_names():
				collection = db[name]
				if collection.find_one_and_replace(filter, data) == None:
					collection.insert_one(data)





















class Mongolo_ModelChunk():
	def __init__(self, url:str="mongodb://localhost:27017/"):
		self.client = pymongo.MongoClient(url)
		self.debug = self.Debug(self)


	class Debug():
		def __init__(self, ModelChunk):
			self.ModelChunk = ModelChunk

		def radius_count(self, radius):
			def gc_2d(radius):
				if radius == 0:
					return 1
				return radius * 4 + gc_2d(radius-1)
			def gc_3d(origin, index):
				if origin == index:
					return gc_2d(index)
				return gc_2d(index) * 2 + gc_3d(origin, index + 1)
			return gc_3d(radius, 0) * 4096
		
		def radius_countD(self, radius):
			def gc_2d(radius):
				if radius == 0:
					return 1
				return radius * 4 + gc_2d(radius-1)
			def gc_3d(origin, index):
				if origin == index:
					return gc_2d(index)
				return gc_2d(index) * 2 + gc_3d(origin, index + 1)
			return gc_3d(radius, 0)


		def random_block(self, name=None, x=None, y=None, z=None, meta=None):
			if name is None:
				name = random.choice(blocks)
			if y is None:
				y = random.randint(0, 0xFFFFFFFF)
			if x is None:
				x = random.randint(0, 0xFFFFFFFF)
			if z is None:
				z = random.randint(0, 0xFFFFFFFF)
			if meta is None:
				meta = random.randint(0, 0xFFFFFFFF)
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
				chunk.connect(world)
				chunk.db.drop()
				chunk.db.insert_many(chunk.data)

				counter += 1
				p = (counter / len) * 100
				if debug and b + 1 < p:
					b = int(p)
					sys.stdout.write("\rfill progress : {}%".format(b))
		else:
			chunks.connect(world)
			chunks.db.drop()
			chunks.db.insert_many(chunk["data"])

		if debug:
			sys.stdout.write("\rfill progress : 100%\n")
		return counter

	def drop(self, world:str):
		db = self.client[world]
		for name in db.list_collection_names():
			db.drop_collection(name)

	def find(self, filter:dict, world:str, chunk:Chunk):
		chunk.connect()
		return chunk.db.find(filter)