import socket
from BasicDB import Mongolo_ModelX
from inputs import get_gamepad
import threading
import asyncio
import pymongo
import random
import time
import re


mongoloClient = Mongolo_ModelX("mongodb://localhost:27017/")





mongoloClient.drop("overworld")

r = 16
t = time.time()
c = mongoloClient.debug.fill_up("overworld", r)

print("{} object added to the database in {}s".format(c, time.time() - t))
