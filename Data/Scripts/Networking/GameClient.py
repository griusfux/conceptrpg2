# $Id$

# Description: The game client
# Contributers: Mitchell Stokes

from Scripts.Networking import parse_request_client, NET_ENCODING
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
		
		self.is_host = False
		
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.setblocking(0)
		
		self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp.settimeout(0)
		
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
			self.tcp.send(bytes(self.user+' register ', NET_ENCODING))
			
			cmd, data = self.receive_message(self.tcp, 5)
			
			data = data.split()
			
			if cmd == 'setup':
				print("Changing username to: "+data[0])
				self.user = data[0]
				
				self.is_host = (int(data[1]) != 0)
				
			self.send_message('register_udp')

	def send_message(self, msg, byte_data=b'', timeout=1):
		if timeout:
			self.udp.settimeout(timeout)
		self.udp.sendto(bytes(self.user+' '+msg, NET_ENCODING)+b' '+byte_data, self.addr)
		if timeout:
			self.udp.setblocking(0)
		
	def receive_message(self, s=None, timeout=0):
		if not s:
			s = self.udp
		
		if timeout: s.settimeout(timeout)
	
		try:
			rdata = s.recv(BUFF)
			# if client_addr != self.addr:
				# print(client_addr, self.addr)
				# raise socket.error
			if timeout: s.setblocking(0)
			return parse_request_client(rdata)
		except socket.error as d:
			if timeout: s.setblocking(0)
			return (None, None)