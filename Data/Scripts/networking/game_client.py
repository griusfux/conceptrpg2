# $Id$

# Description: The game client
# Contributers: Mitchell Stokes

from Scripts.networking import NET_ENCODING, COMMAND_SEP

import time
import enet

TIMEOUT = 5

class GameClient:
	"""The client for game networking"""
	
	def __init__(self, id, addr):
		self._id = id
		self.bytes_id = bytes(id, NET_ENCODING)
		self.host = enet.Host(None, 1, 0, 0, 0)
		self.peer = self.host.connect(enet.Address(*addr), 1)
		self.connect_time = time.time()
		
		self.connected = False
		self.registered = False
		self.server_addr = None
		
	@property
	def id(self):
		return self._id
	
	@id.setter
	def id(self, value):
		self._id = value
		self.bytes_id = bytes(value, NET_ENCODING)
		
	def disconnect(self):
		self.send(b'dis'+COMMAND_SEP)
		self.host.flush()
		
	def restart(self, id, addr):
		self.id = id

		self.host = enet.Host(None, 1, 0, 0, 0)
		self.peer = self.host.connect(enet.Address(*addr), 1)
		self.connect_time = time.time()
	
		self.connected = False
		self.server_addr = None
	
	def run(self):
		if not self.connected and time.time() - self.connect_time > TIMEOUT:
			self.server_addr = "0.0.0.0"
			self.connected = False
			return
			
	
		event = self.host.service(0)
		
		if event.type == enet.EVENT_TYPE_CONNECT:
			self.connected = True
			self.server_addr = event.peer.address.host
			self.send(b'register')
		elif event.type == enet.EVENT_TYPE_DISCONNECT:
			self.connected = False
			self.server_addr = "0.0.0.0"
		elif event.type == enet.EVENT_TYPE_RECEIVE:
			data = event.packet.data
			if data.startswith(b'cid'+COMMAND_SEP):
				self.id = str(data.split(COMMAND_SEP)[1], NET_ENCODING)
				print("ID set to", self.id)
				self.registered = True
			else:
				return data
			
		return None
		
	def send(self, msg):
		"""Send a message and user name to the server"""
		
		if not self.connected:
			return
		
		self.peer.send(0, enet.Packet(b" ".join((self.bytes_id, msg))))
				