import socket
from BasicDB import Mongolo_ModelX
from inputs import get_gamepad
import threading
import asyncio
import pymongo
import random
import time
import re








def get_count(radius):
	_3d = gc_3d(radius, 0)

	return _3d

def gc_3d(r_org, r_index):
	if r_org == r_index:
		return gc_2d(r_index)
	return gc_2d(r_index) * 2 + gc_3d(r_org, r_index + 1)


def gc_2d(radius):
	if radius == 0:
		return 1
	return radius * 4 + gc_2d(radius-1)

#mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
mongoloClient = Mongolo_ModelX("mongodb://localhost:27017/")


#mydb = mongoClient["overworld_blocks"]


mongoloClient.drop("overworld")

r = 16
t = time.time()
c = mongoloClient.debug.fill_up("overworld", r)

print("{} object added to the database in {}s".format(c, time.time() - t))

#t = time.time()
#res = mongoloClient.debug.radius_count(r)


#print("{} object counted in {}s".format(res, time.time() - t))