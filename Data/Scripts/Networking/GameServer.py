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
import socket

from Scripts.Networking import parse_request, NET_ENCODING

class GameServerHandler(BaseRequestHandler):
	""" Handles client connections"""
	
	def handle(self):
		
		print("SERVER Message from %s: %s" % (self.client_address[0], self.request[0]))
		
		cmd, data = parse_request(self.request[0])
		sock = self.request[1]
		server = self.server
		
		if cmd == "ping":
			# Simple ping/pong test to test the connection
			self.send_message('pong')
			
		elif cmd == "register":
			# Register the user
			if data[0] not in server.clients:
				server.clients[data[0]] = self.client_address
				
			# If this is the first user, it's the host
			if len(server.clients):
				server.host = data[0]

		elif cmd == "send_map":
			server.map.append(data)
			
		elif cmd == "get_map":
			for i in server.map:
				self.send_message('map '+i)
				
			self.send_message('end_map')
		
	def send_message(self, msg, byte_data=b''):
		print("SERVER Message to %s: %s" % (self.client_address[0], bytes(msg, NET_ENCODING)+byte_data))
		self.request[1].sendto(bytes(msg, NET_ENCODING)+b' '+byte_data, self.client_address)
		
	def broadcast(self, msg, client):
		sock = self.request[1]
		
		for client in self.server.clients:
			if client != self.client_address:
				sock.sendto(msg, client)
		

class GameServer(UDPServer):
	"""The game server"""
	
	def __init__(self, port):
		print("Starting the server...")
		self.clients = {}
		self.host = None
		self.map = []
		UDPServer.__init__(self, ('', port), GameServerHandler)