# $Id$

# Description: The game server
# Contributers: Mitchell Stokes

try:
	from socketserver import UDPServer, BaseRequestHandler
	import pickle
except ImportError:
	from SocketServer import UDPServer, BaseRequestHandler
	import cPickle as pickle
	
import re

class GameServerHandler(BaseRequestHandler):
	""" Does stuff??"""
	
	def handle(self):
		
		print("SERVER Message from %s: %s" % (self.client_address[0], self.request[0]))
		
		req_str = str(self.request[0], "utf8")
		
		regex = re.compile('(.*?)( )(.*)', re.DOTALL)
		cmd = regex.match(req_str).group(1)
		data = regex.match(req_str).group(3)
		
		if cmd == "register":
			if self.client_address not in self.server.clients:
				self.server.clients.append(self.client_address)
				
			self.request[1].sendto(b'pong', self.client_address)
		elif cmd == "map":
			self.server.map.append(data)
		elif cmd == "get_map":
			for i in self.server.map:
				self.request[1].sendto(i, self.client_address)
		#self.broadcast(self.request[0], self.client_address)
		
	def broadcast(self, msg, client):
		socket = self.request[1]
		for client in self.server.clients:
			if client != self.client_address:
				socket.sendto(msg, client)
		

class GameServer(UDPServer):
	"""The game server"""
	
	def __init__(self, addr):
		print("Starting the server...")
		self.clients = []
		self.map = []
		UDPServer.__init__(self, addr, GameServerHandler)