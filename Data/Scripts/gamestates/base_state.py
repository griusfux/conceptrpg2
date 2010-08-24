# $Id$

# This class shouldn't be used, it just handles some common state things.
# However, it is a good place to copy/paste from when starting a new state. ;)

class BaseState:
	"""Base gamestate"""
	
	def __init__(self, main, is_server=False):
		"""BaseState Constructor"""
		
		if is_server:
			self.server_init(main)
			self.run = self.server_run
		else:
			self.client_init(main)
			self.run = self.client_run
			
	def cleanup(self, main):
		"""Do any cleanup here (override if you need it)"""
		pass
					
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		pass
		
	def client_run(self, main):
		"""Client-side run method"""
		pass
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main):
		"""Server-side run method"""
		pass

	##########
	# Other
	##########
	
	# Empty ---