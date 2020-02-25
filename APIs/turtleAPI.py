from threading import Thread
from flask import Flask, escape, request, Response
import socket
import time







class ServerThread(Thread):
	def __init__(self, mongoloClient_):
		super(ServerThread, self).__init__()
		self.mongoloClient = mongoloClient_
		self.cleaner = CleanerThread()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('', 8191))
		self.sock.listen(5)
		self.sock.settimeout(1)
		self.alive = True

	def __del__(self):
		print("server __del__")

	def stop(self):
		self.alive = False

	def run(self):
		self.cleaner.start()
		while self.alive:
			try:
				client, addr = self.sock.accept()
			except socket.timeout as e:
				continue
			try:
				cthread = ClientThread(client, self.mongoloClient)
			except Exception as e:
				client.close()
				print(e)
				continue
			cthread.start()
			self.cleaner.add(cthread)
		self.sock.close()
		self.cleaner.stop()
		self.cleaner.join()


class CleanerThread(Thread):
	def __init__(self):
		super(CleanerThread, self).__init__()
		self.threads = []
		self.alive = True

	def __del__(self):
		print("cleaner __del__")

	def add(self, thread):
		self.threads.append(thread)

	def stop(self):
		self.alive = False

	def run(self):
		while self.alive:
			for t in self.threads:
				if not t.is_alive():
					print("a thread died")
					self.threads.remove(t)
					t.join()
		for t in self.threads:
			t.stop()
		for t in self.threads:
			t.join()
			self.threads.remove(t)

class ClientThread(Thread):
	def __init__(self, client_, mongoloClient_):
		self.client = client_
		self.mongoloClient = mongoloClient_
		self.client.settimeout(5.0)
		self.alive = True
		self.dataBuild()
		super(ClientThread, self).__init__()

	def __del__(self):
		print("client __del__")

	def setStatusText(self, text):
		pkg = bytearray([0x01, len(str(text))])
		pkg += bytearray(str(text), "utf-8")
		self.client.send(pkg)

	def move(self, x, y, z):
		msg = "{}|{}|{}".format(x, y, z)
		pkg = bytearray([0x02, len(msg)])
		pkg += bytearray(msg, "utf-8")
		self.client.send(pkg)
		pkg = self.client.recv(64)
		if pkg != b"ok":
			raise("move not ok")

	def getOffset(self):
		self.client.send(bytearray([0x03, 0x00]))
		data = self.client.recv(64).decode("utf-8")
		print("data : {}".format(data))
		data = data.split("|")
		return {"x":int(data[0]), "y":int(data[1]), "z":int(data[2])}

	def setLightColor(self, r, g, b):
		pkg = bytearray([0x04, 0x03, r, g, b])
		self.client.send(pkg)

	def scanContentsAt(self, x, y, z):
		msg = "{}|{}|{}".format(x, y, z)
		pkg = bytearray([0x05, len(msg)])
		pkg += bytearray(msg, "utf-8")
		self.client.send(pkg)
		pkg = self.client.recv(64)
		if pkg != b"ok":
			raise("scan not ok")

	def ping(self):
		pkg = bytearray([0xFF, 0x04])
		pkg += bytearray("ping", "utf-8")
		self.client.send(pkg)
		pkg = self.client.recv(64)
		if msg != b"pong":
			raise(BaseException("pong not ok"))

	def dataBuild(self):
		self.setLightColor(0xFF, 0x00, 0x00)
		coords = self.getOffset()
		self.setLightColor(0x00, 0xFF, 0x00)

	def dataDestroy(self):
		return

	def stop(self):
		self.alive = False
		self.dataDestroy()
		self.client.close()

	def run(self):
		while self.alive:
			msg = None
			try:
				msg = self.client.recv(64)
			except socket.timeout as e:
				try:
					self.ping()
				except Exception as e:
					print(1)
					print(e)
					return self.stop()
			except socket.error as e:
				return self.stop()
			except Exception as e:
				try:
					return self.stop()
				except Exception as e:
					print(2)
					print(e)
					return self.stop()
			if msg and msg == b"ping":
				print(msg)
				self.client.send(b"pong")
		return self.stop()



import sys


def initTurtleAPI(app, mongoloClient):
	





	s = ServerThread(mongoloClient)
	s.start()
	return s
