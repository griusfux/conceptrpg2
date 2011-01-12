# $Id$

# Description: The game server
# Contributers: Mitchell Stokes


from Scripts.networking import NET_ENCODING
from Scripts.gamestate_manager import GameStateManager

import traceback
import time
import enet

class NetPlayer():
		"""Class for handling player data"""
		
		def __init__(self, race, pos, ori):
			self.race = race
			self.position = pos
			self.orientation = ori

class ClientHandle():
	"""Class for handling client requests"""
	
	def __init__(self, server, client_id, peer):
		self.server = server
		self.last_update = time.time()
		self.id = client_id
		self.peer = peer
		
		self.state_manager = GameStateManager("DungeonGeneration", self.server.main, is_server=True)
		
	def handle_request(self, data, peer):
		self.peer = peer
		
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
		
		self.peer.send(0, enet.Packet(bytes(data, NET_ENCODING)))

class GameServer():
	"""The game server"""
	
	def __init__(self, port, timeout):
				
		# The "main" dict for storing globals
		self.main = {}
		
		# Store the server itself (for RPC stuff)
		self.main['server'] = self
		
		# Client info
		self.main['clients'] = {}
		
		# Player info
		self.main['players'] = {}
		
		# The current dungeon
		self.main['dungeon'] = []
		
		# Create the host
		self.host = enet.Host(enet.Address(b'', port), 10, 0, 0, 0)
		
		# How long we wait on players
		self.timeout = timeout
		
		print("Server ready")
		
		# Now run the server
		try:
			while True:
				event = self.host.service(1000)
				
				if event.type == enet.EVENT_TYPE_CONNECT:
					print('Client Connected:', event.peer.address)
				elif event.type == enet.EVENT_TYPE_DISCONNECT:
					self.drop_client(event.peer, "Disconnected")
				elif event.type == enet.EVENT_TYPE_RECEIVE:
					data = str(event.packet.data, NET_ENCODING)
					d = data.split()
					client_id = d[0]
					
					if client_id not in self.main['clients']:
						self.register_client(client_id, event.peer)
					
					if d[1] == 'register': continue

					self.main['clients'][client_id].handle_request(data, event.peer)

		except Exception:
			traceback.print_exc()
		except:
			# Grabs the KeyboardInterrupt
			pass
			
		print("Server exiting...")
					
	def register_client(self, client_id, peer):
		"""Registers a client"""
		# Make the id unique
		while client_id in self.main['clients']:
			client_id += '_'

		peer.send(0, enet.Packet(b'cid:'+bytes(client_id, NET_ENCODING)))
		self.main['clients'][client_id] = ClientHandle(self, client_id, peer)
		print("%s Registered as %s" % (peer.address, client_id))
					
	def drop_client(self, peer, reason):
		"""Drop a client"""
		
		for cid, client in self.main['clients'].items():
			if client.peer == peer:
				client_id = cid
				break
		else:
			# The player never fully connected, ignore the drop
			return
		
		if client_id in self.main['clients']:
			print(client_id, reason)
			del self.main['clients'][client_id]
			
			try:
				del self.main['players'][client_id]
			except KeyError:
				print("Warning: %s not found in players list when dropping client" % client_id)
			
	def add_player(self, client_id, race, position, orientation):
		"""Adds a player to the player dictionary to cache position and orientation data.
		
			Having this method avoids having to import the NetPlayer class into gamestates
		"""
		
		self.main['players'][client_id] = NetPlayer(race, position, orientation)
		
	def send(self, data):
		"""Alias to broadcast for use with RPC"""
		self.broadcast(data)
		
	def broadcast(self, data):
		"""Broadcast a message to all of the clients"""
		
		# Uncomment to get debug prints
		# print("BROADCAST:", data)
		
		for cid, client in self.main['clients'].items():
			client.peer.send(0, enet.Packet(bytes(data, NET_ENCODING)))
			