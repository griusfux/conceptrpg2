# $Id$

# Description: The game client
# Contributers: Mitchell Stokes

from Scripts.Networking import parse_request, NET_ENCODING
import pickle
import re
import socket

# The buffer size to use
BUFF = 4096

class GameClient:
	"""The client for game networking"""
	
	def __init__(self, user, addr):
		self.user = user
		self.addr = addr
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# Try to ping the server
		self.socket.settimeout(5)
		self.send_message('ping')
		print('Attempting to ping the server...')
		try:
			self.socket.recv(BUFF)
			print('Reply received')
			self.connected = True
		except socket.timeout:
			print('The request to the server timed out.')
			self.connected = False
		except socket.error as d:
			print(d)
			print('The server could not be reached')
			self.connected = False
		finally:
			# Keep the socket as non-blocking unless needed otherwise
			self.socket.setblocking(0)
			
		if self.connected:
			self.send_message('register '+user)
		
	def send_message(self, msg, byte_data=b'', timeout=1):
		if timeout:
			self.socket.settimeout(timeout)
		self.socket.sendto(bytes(msg, NET_ENCODING)+b' '+byte_data, self.addr)
		if timeout:
			self.socket.setblocking(0)
		
	def receive_message(self):
		try:
			rdata = self.socket.recv(BUFF)
			return parse_request(rdata)
		except socket.error as d:
			return (None, None)