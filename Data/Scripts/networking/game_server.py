# $Id$

# Description: The game server
# Contributers: Mitchell Stokes

# from socketserver import UDPServer, BaseRequestHandler

from Scripts.networking import NET_ENCODING
from Scripts.gamestate_manager import GameStateManager

import socket
import select
import time

BUFFER = 4096

# class GameRequestHandler(BaseRequestHandler):
	# """Handles incoming requests"""
	
class ClientHandle():
	"""Class for handling client requests"""
	
	def __init__(self, server, client_id, client_addr):
		self.server = server
		self.last_update = time.time()
		self.id = client_id
		self.addr = client_addr
		
		self.state_manager = GameStateManager("DungeonGeneration", self.server.main, is_server=True)
		
	def handle_request(self, data, client_addr):
		self.last_update = time.time()
		self.addr = client_addr
		
		if data:
			# Clean up the data a little
			self.id = data.split()[0]
			self.data = " ".join([i for i in data.split()[1:]])
		
			# print("Message %s from %s" % (data, client_addr))
			
			# for input in self.data.split():
				# if input.startswith('state'):
					# state = input.replace('state', '')
					# if state == 'cmbt':
						# state = CombateState
					# elif state == 'dflt':
						# state = DefaultState
						
					# self.server.main['state'] = state(self.server.main, True)
			
			# self.server.main['state'].run(self, self.server.main)
			self.state_manager.run(self.server.main, self)
			
	def send(self, data):
		"""Send a message to the client"""
		
		self.server.socket.sendto(bytes(data, NET_ENCODING), self.addr)

class GameServer():
	"""The game server"""
	
	def __init__(self, port, timeout):
		#UDPServer.__init__(self, ('', port), GameRequestHandler)
				
		# The "main" dict for storing globals
		self.main = {}
		
		# Store the server itself (for RPC stuff)
		self.main['server'] = self
		
		# Client info
		self.main['clients'] = {}
		
		# The current dungeon
		self.main['dungeon'] = []
		
		# Create the socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(('', port))
		
		# How long we wait on players
		self.timeout = timeout
		
		# Startup the state manager with the default state
		# self.state_manager = GameStateManager("Default", self.main, is_server=True)
		
		print("Server ready")
		
		# Now run the server
		while True:
			r, w, e = select.select([self.socket], [], [], 0.01)
			if r:
				try:
					data, client_addr = self.socket.recvfrom(BUFFER)
					data = str(data, NET_ENCODING)
				except socket.error as e:
					print(e)
					data = ""
				
				if data:
					d = data.split()
					client_id = d[0]
					
					if client_id not in self.main['clients']:
						self.register_client(client_id, client_addr)
					elif self.main['clients'][client_id].addr != client_addr:
						# Make the client_id unique
						while client_id in self.main['clients']:
							client_id = client_id + "_"
							
						self.register_client(client_id, client_addr)
					
					if len(d) > 1 and d[1] == "ping":
						self.socket.sendto(b"pong", client_addr)
						self.main['clients'][client_id].last_update = time.time()
					else:
						self.main['clients'][client_id].handle_request(data, client_addr)
				
			# Check the status of the clients
			for cid in [i for i in self.main['clients'].keys()]:
				if time.time() - self.main['clients'][cid].last_update > self.timeout:
					self.broadcast("to:"+cid)
					self.drop_client(cid, "Timed Out")
					
	def register_client(self, client_id, client_addr):
		"""Registers a client"""
		
		print(client_id, "Registered")
		self.socket.sendto(b"cid:"+bytes(client_id, NET_ENCODING), client_addr)
		self.main['clients'][client_id] = ClientHandle(self, client_id, client_addr)
					
	def drop_client(self, client_id, reason):
		"""Drop a client"""
		
		if client_id in self.main['clients']:
			print(client_id, reason)
			del self.main['clients'][client_id]
		
	def send(self, data):
		"""Alias to broadcast for use with RPC"""
		self.broadcast(data)
		
	def broadcast(self, data):
		"""Broadcast a message to all of the clients"""
		
		# Uncomment to get debug prints
		# print("BROADCAST:", data)
		
		for cid, client in self.main['clients'].items():
			self.socket.sendto(bytes(data, NET_ENCODING), client.addr)
			