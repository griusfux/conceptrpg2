# $Id$

# Description: The game client
# Contributers: Mitchell Stokes

from Scripts.Networking import NET_ENCODING

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
		
		self.last_update = time.time()
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
		
		try:
			data, addr = self.socket.recvfrom(BUFFER)
			
			if not self.server_addr:
				print("Server found")
				print(data, addr)
				self.last_update = time.time()
				self.server_addr = addr
				self.connected = True
			elif self.server_addr == addr:
				self.last_update = time.time()
				data = str(data, NET_ENCODING).split()
				val = (data[0], data[1:])

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
				