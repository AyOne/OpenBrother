import pymongo
import time
import re
import random
import unittest
import sys
import math


blocks = ["minecraft:air", "minecraft:ore"]

class Mongolo_ModelX():
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

		def random_chunk(self, x=None, y=None, z=None):
			return []

		def new_chunk(self, world:str):
			return []


	def getChunkFromBlock(self, block:dict, world:pymongo.database.Database, db:bool=True):
		chunk = {
			"x":math.floor(block["x"] / 16),
			"y":math.floor(block["y"] / 16),
			"z":math.floor(block["z"] / 16),
			"chunk":None
		}
		if db:
			chunk["chunk"] = world["%d-%d-%d" % (chunk["x"], chunk["y"], chunk["z"])]
		return chunk

	def isInChunk(self, block:dict, chunk:dict):
		if math.floor(block["x"] / 16) != chunk["x"]:
			return False
		elif math.floor(block["y"] / 16) != chunk["y"]:
			return False
		elif math.floor(block["z"] / 16) != chunk["z"]:
			return False
		return True

	def findNreplace(self, block:dict, world:str):
		chunk = blockToChunk(data, self.client[world])
		filter = {
			"x":block["x"] - chunk["x"],
			"y":block["y"] - chunk["y"],
			"z":block["z"] - chunk["z"],
		}
		block["x"] = filter["x"]
		block["y"] = filter["y"]
		block["z"] = filter["z"]
		if chunk["chunk"].find_one_and_replace(filter, block) == None:
			chunk["chunk"].insert_one(block)

	def findNreplace_chunk(self, blocks:list, world:str):
		if len(blocks) == 0:
			return
		ref_chunk = self.getChunkFromBlock(block[0], self.client[world])
		for block in blocks:
			if not isInChunk(block, ref_chunk):
				raise Exception("block list contains blocks from multiple chunks")
		for block in blocks:
			filter = {
				"x":block["x"] - chunk["x"],
				"y":block["y"] - chunk["y"],
				"z":block["z"] - chunk["z"],
			}
			block["x"] = filter["x"]
			block["y"] = filter["y"]
			block["z"] = filter["z"]
			if ref_chunk["chunk"].find_one_and_replace(filter) == None:
				ref_chunk["chunk"].insert_one(block)

	def find(self, filter:dict, world:str, id:bool=False):
		chunk = getChunkFromBlock(filter, self.client[world])
		filter_ = {
			"x":filter["x"] - chunk["x"],
			"y":filter["y"] - chunk["y"],
			"z":filter["z"] - chunk["z"],
		}
		finalData = list(chunk["chunk"].find(filter_))
		if not id:
			for data in finalData:
					del data["_id"]
		return finalData

	def find_chunk(self, filter:dict, world:str, id:bool=False):
		chunk = getChunkFromBlock(filter, self.client[world])
		finalData = list(chunk["chunk"].find({}))
		if not id:
			for daya in finalData:
				del data["_id"]
		return finalData