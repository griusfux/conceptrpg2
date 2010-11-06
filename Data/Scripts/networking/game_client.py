# $Id$

# Description: The game client
# Contributers: Mitchell Stokes

from Scripts.networking import NET_ENCODING

import socket
import time

# The buffer size to use
BUFFER = 4096
TIMEOUT = 5

class GameClient:
	"""The client for game networking"""
	
	def __init__(self, id, addr):
		self.id = id
		self.addr = addr
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setblocking(0)
		
		self.connected = False
		self.server_addr = None
		
		self.last_update = self.last_ping = time.time()
		self.socket.sendto(bytes(id, NET_ENCODING), addr)
		
	def restart(self, id, addr):
		self.id = id
		self.addr = addr
	
		self.connected = False
		self.server_addr = None
		
		self.last_update = time.time()
		self.socket.sendto(bytes(self.id, NET_ENCODING), self.addr)
		
	def run(self):
		"""Try to get data from the server"""
		val = None
		
		# If we haven't yet connected, keep poking for a server
		if not self.connected:
			self.socket.sendto(bytes(self.id, NET_ENCODING), self.addr)
		elif time.time() - self.last_ping > 1.0:
			# Let the server know we're still alive
			self.send("ping")
			self.last_ping = time.time()
		
		try:
			data, addr = self.socket.recvfrom(BUFFER)
			
			if not self.server_addr:
				print("Server found", addr)
				self.last_update = time.time()
				self.server_addr = addr
				self.connected = True
				
				# Do a name change if necessary
				data = str(data, NET_ENCODING)
				
				if data.startswith("cid:"):
					self.id = data.split(':')[1]
					print("ID set to", self.id)
			elif self.server_addr == addr:
				self.last_update = time.time()
				data = str(data, NET_ENCODING)
				if data != "pong": val = data
				# data = str(data, NET_ENCODING).split()
				# val = (data[0], data[1:])

		except socket.error:
			pass
							
		if time.time() - self.last_update > TIMEOUT:
			print("Connection to the server timed out")
			self.server_addr = "0.0.0.0"
			self.connected = False
			
		return val
		
	def send(self, msg):
		"""Send a message and user name to the server"""
		
		if not self.connected:
			return
		
		self.socket.sendto(bytes(self.id+" "+msg, NET_ENCODING), self.server_addr)
				