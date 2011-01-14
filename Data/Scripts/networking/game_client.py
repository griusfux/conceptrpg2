# $Id$

# Description: The game client
# Contributers: Mitchell Stokes

from Scripts.networking import NET_ENCODING

import time
import enet

TIMEOUT = 5

class GameClient:
	"""The client for game networking"""
	
	def __init__(self, id, addr):
		self.id = id
		self.host = enet.Host(None, 1, 0, 0, 0)
		self.peer = self.host.connect(enet.Address(*addr), 1)
		self.connect_time = time.time()
		
		self.connected = False
		self.registered = False
		self.server_addr = None
		
	def disconnect(self):
		self.send('dis:')
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
			self.send('register')
		elif event.type == enet.EVENT_TYPE_DISCONNECT:
			self.connected = False
			self.server_addr = "0.0.0.0"
		elif event.type == enet.EVENT_TYPE_RECEIVE:
			data = str(event.packet.data, NET_ENCODING)
			if data.startswith('cid:'):
				self.id = data.split(':')[1]
				print("ID set to", self.id)
				self.registered = True
			else:
				return data
			
		return None
		
	def send(self, msg):
		"""Send a message and user name to the server"""
		
		if not self.connected:
			return
		
		self.peer.send(0, enet.Packet(bytes(self.id+" "+msg, NET_ENCODING)))
				