# $Id$

# Description: The game server
# Contributers: Mitchell Stokes

try:
	from socketserver import TCPServer, UDPServer, ThreadingMixIn, BaseRequestHandler
except ImportError:
	from SocketServer import TCPServer, UDPServer, ThreadingMixIn, BaseRequestHandler
	
import re
import socket
import select
import threading
import time

from Scripts.Networking import parse_request, NET_ENCODING

class GameServerBaseHandler(BaseRequestHandler):
	""" Handles udp client connections"""

	accepted_cmds = [
			'ping',
			'register',
			'register_udp',
			'reset_map',
			'set_map',
			'get_map',
			'update_player',
			'chat'
			]
	
	def handle(self):
		user, cmd, data = parse_request(self.data)
		self.user = user
		
		if cmd in self.accepted_cmds:
			getattr(self, cmd)(data)
		else:
			print("Command not found " +cmd)

	def broadcast(self, msg, exclude='self'):
		if exclude == 'self': exclude = self.user
		for client in self.server.clients:
			if client != exclude:
				self.send_message(msg, client=self.server.clients[client])
				
	def is_host(self):	
		return True if self.server.host == self.user else False
				
	def client_from_addr(self, addr=None):
		if not addr: addr = self.client_address
		
		for client in self.server.clients:
			if addr in self.server.clients[client]:#self.server.clients[client][0] == addr:
				return client
				
		return None
	
	#
	# Commands start here
	#		
	def register(self, data):
		"""Register the user"""
		user = self.user					
		
		# Make the name unique
		while user in self.server.clients:
			user = user + "_"
			
		# If this is the first user, it's the host
		if not self.server.host:
			self.server.host = user
			host = 1
		else:
			host = 0

		print("SERVER registering %s as %s. Is host? %s" % (self.user, user, 'True' if host == 1 else 'False'))
		self.server.clients[user] = [self.client_address, None]
		self.send_message("setup %s %s" % (user, host))
		
	def register_udp(self, data):
		"""Register the client's udp addr"""
		self.server.clients[self.user][1] = self.client_address
		
	def reset_map(self, data):
		"""Start a new map if the client is the host"""
		
		if self.is_host():
			self.server.map = []
			
	def set_map(self, data):
		"""Add new map tiles if the client is the host"""
		
		if self.is_host():
			self.server.map.append(data)
			
	def get_map(self, data):
		"""Send the map tiles to the player"""
		
		for i in self.server.map: self.send_message('map '+i)
		
		self.send_message('end_map')
		
	def update_player(self, data):
		"""Send updated player data to all of the clients"""
		
		self.broadcast('update_player '+data)
		
class GameServerTCPHandler(GameServerBaseHandler):
	"""Handles tcp client connections"""
			
	def handle(self):
		self.socket = self.request
		self.data = self.socket.recv(1024)
		
		while self.data:
			print("SERVER TCP Message from %s: %s" % (self.client_address[0], self.data))
			
			GameServerBaseHandler.handle(self)
			
			try:
				self.data = self.socket.recv(1024)
			except socket.error:
				self.data = ""
			
		user = self.client_from_addr()
		if user:
			print("SERVER disconnect: %s" % (user))
			del self.server.clients[user]
			self.broadcast('disconnect '+user)
		else:
			print("SERVER client disconnected but not found in list: (%s, %s)" % (self.client_address[0], self.client_address[1]))

	def send_message(self, msg, byte_data=b'', client=None):
		if not client: client = self.server.clients[self.user]
		print("SERVER TCP Message to %s: %s" % (client[0][0], bytes(msg, NET_ENCODING)+byte_data))
		self.request.sendto(bytes(msg, NET_ENCODING)+b' '+byte_data, client[0])
		
class GameServerUDPHandler(GameServerBaseHandler):
	"""Handles udp client connections"""
	
	def setup(self):
		self.socket = self.request[1]
		self.data = self.request[0]
	
		print("SERVER UDP Message from %s: %s" % (self.client_address[0], self.data))
		
	def send_message(self, msg, byte_data=b'', client=None):
		if not client: client = self.server.clients[self.user]
		print("SERVER UDP Message to %s: %s" % (client[1][0], bytes(msg, NET_ENCODING)+byte_data))
		self.request[1].sendto(bytes(msg, NET_ENCODING)+b' '+byte_data, client[1])
		
class GameServerTCP(ThreadingMixIn, TCPServer):
	"""Tcp part of the game server"""
	
	def __init__(self, port, server):
		self.server = server
		self.daemon_threads = True
		TCPServer.__init__(self, ('', port), GameServerTCPHandler)
		
	def finish_request(self, request, client_address):
		"""Finish one request by instantiating RequestHandlerClass."""
		self.RequestHandlerClass(request, client_address, self.server)		
		
class GameServerUDP(UDPServer):
	"""UDP part of the game server"""
	
	def __init__(self, port, server):
		self.server = server
		UDPServer.__init__(self, ('', port), GameServerUDPHandler)
		
	def finish_request(self, request, client_address):
		"""Finish one request by instantiating RequestHandlerClass."""
		self.RequestHandlerClass(request, client_address, self.server)
		
class GameServer():
	"""The game server"""
	
	def __init__(self, port):
		print("Starting the server...")
		self.clients = {}
		self.host = None
		self.map = []
		self.port = port
		
		self.tcp = GameServerTCP(port, self)
		
		self.tcp_thread = threading.Thread(target=self.tcp.serve_forever)
		self.tcp_thread.setDaemon(True)
		self.tcp_thread.start()
		
		print("TCP ready")
		
		self.udp = GameServerUDP(port, self)
		
		self.udp_thread = threading.Thread(target=self.udp.serve_forever)
		self.udp_thread.setDaemon(True)
		self.udp_thread.start()
		
		print("UDP ready")
		
		while self.tcp._BaseServer__serving and self.udp._BaseServer__serving:
			time.sleep(10)
			print("\nCurrent clients:")
			for i in self.clients:
				print("%s : (%s, %s)" % (i, self.clients[i][0], self.clients[i][1]))
				
			print()

	def __del__(self):
		self.tcp.shutdown()
		self.udp.shutdown()
		