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
		
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.setblocking(0)
		
		self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp.settimeout(5)
		
		try:
			self.tcp.connect(addr)
			print('Successfuly connected to the server')
			self.connected = True
		except socket.timeout:
			print('The request to the server timed out.')
			self.connected = False
		except socket.error as d:
			print(d)
			print('The server could not be reached')
			self.connected = False
		finally:
			self.tcp.setblocking(0)
			
		if self.connected:
			self.tcp.send(bytes('register '+self.user, NET_ENCODING))
		
	def __del__(self):
		self.tcp.close()
		self.udp.close()

	def send_message(self, msg, byte_data=b'', timeout=1):
		if timeout:
			self.udp.settimeout(timeout)
		self.udp.sendto(bytes(msg, NET_ENCODING)+b' '+byte_data, self.addr)
		if timeout:
			self.udp.setblocking(0)
		
	def receive_message(self):
		try:
			rdata, client_addr = self.udp.recvfrom(BUFF)
			# if client_addr != self.addr:
				# print(client_addr, self.addr)
				# raise socket.error
			return parse_request(rdata)
		except socket.error as d:
			return (None, None)