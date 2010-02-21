# $Id$

# Description: The game server
# Contributers: Mitchell Stokes

try:
	from socketserver import UDPServer, BaseRequestHandler
except ImportError:
	from SocketServer import UDPServer, BaseRequestHandler

class GameServerHandler(BaseRequestHandler):
	""" Does stuff??"""
	
	def handle(self):
		if self.client_address not in self.server.clients:
			self.server.clients.append(self.client_address)
		
		print("SERVER Message from %s: %s" % (self.request[1], self.request[0]))
		self.broadcast(self.request[0], self.client_address)
		
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
		UDPServer.__init__(self, addr, GameServerHandler)