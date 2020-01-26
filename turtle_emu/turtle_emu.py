import time
import requests
import json
import random

url = "http://localhost:8190"



def rebuild():
	a = requests.get("{}/debug/rebuild?data={}".format(url, json.dumps({
			"radius":3
		})))
	print(a)


def listeTypeBlocks():
	a = requests.get("{}/listeTypeBlocks?data={}".format(url, json.dumps({
			"chunks":[
				{
					"x":2,
					"z":0
				}
			],
			"filter":{},
			"dim":"overworld"
		})))
	print(a)


def getRef():
	a = json.loads(requests.get("{}/getRef?data={}".format(url, json.dumps({"filter":{}}))).text)
	print(a)
	return a["ref"]



def random_block(blocks=[], name=None, x=None, y=None, z=None, meta=None):
	if name is None:
		name = random.choice(blocks)
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

def random_chunk(blocks):
	data = []
	for x_ in range(16):
		for y_ in range(16):
			for z_ in range(16):
				data.append(random_block(blocks=blocks, x=x_, y=y_, z=z_))
	return data










def insertChunk():
	refs = getRef()
	blocks = []
	for ref in refs:
		blocks.append(ref["id"])
	data = []
	if blocks:
		data = random_chunk(blocks)
	print("???")
	jsondumps = json.dumps({
			"chunk":{"x":100, "y":10, "z":100},
			"data":data,
			"dim":"overworld"
		})
	print(len(jsondumps))
	a = requests.post("{}/insertChunk?data={}".format(url, jsondumps))
	print(a)





input("press any key to continue...")

rebuild()
listeTypeBlocks()
insertChunk()