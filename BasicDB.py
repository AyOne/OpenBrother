import pymongo
import time
import re
import random
import unittest
import sys

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




	def find(self, filter: dict, db:[str, pymongo.database.Database, pymongo.collection.Collection]):
		#if db is a collection, no need for more querrys. low cost
		if type(db) == pymongo.collection.Collection:
			return db.find(filter)
		if type(db) == str:
			db = self.client[db]
		if "x" in filter:
			collection = db[filter["x"]]
			return collection.find(filter)
		else:
			finalData = []
			for name in db.list_collection_names():
				collection = db[name]
				finalData += collection.find(filter)
			return finalData

	def findNreplace(self, data: list, filter: dict, db:[str, pymongo.database.Database, pymongo.collection.Collection]):
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
			collection = db[filter["x"]]
			if collection.find_one_and_replace(filter, data):
				collection.insert_one(data)
		#else... meh. let's querry them all... warning : heavy cost
		else:
			for name in db.list_collection_names():
				collection = db[name]
				if collection.find_one_and_replace(filter, data) == None:
					collection.insert_one(data)