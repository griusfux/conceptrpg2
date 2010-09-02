# $Id$

# This class shouldn't be used directly, it just handles some common state things.
# However, it is a good place to copy/paste from when starting a new state. ;)

class BaseState:
	"""Base gamestate"""
	
	def __init__(self, main, is_server=False):
		"""BaseState Constructor"""
		
		# Store main
		self.main = main
		
		if is_server:
			self.server_init(main)
			self.run = self.server_run
			self.cleanup = self.server_cleanup
		else:
			self.client_init(main)
			self.run = self.client_run
			self.cleanup = self.client_cleanup
			
	def run(self, main):
		# Update main
		self.main = main
		
		self._run(main)
					
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		pass
		
	def client_run(self, main):
		"""Client-side run method"""
		pass
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
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
			
	def server_cleanup(self, main):
		"""Cleanup the server state"""
		pass

	##########
	# Other
	##########
	
	# Empty ---
	
# All states should have a controller interface by which things like the AI system may make use
# of the state. Subclass this controller and override methods as you need them.
class BaseController:
	"""Base controller interface"""
	
	def play_animation(self, character, animation, lock=0):
		"""Instruct the character to play the animation
		
		character -- the charcter who will play the animation
		animation -- the animation to play
		lock -- how long to lock for the animation
		
		"""
		
		pass
		
	def get_targets(self, type, range):
		"""Get targets in a range
		
		type -- the type of area (line, burst, etc)
		range -- the range to grab (integer)
		
		"""
		
		return []
	
	def modify_health(self, character, amount):
		"""Modify the health of the character
		
		character -- the character whose health you want to change
		amount -- the amount to change the health by (negative for damage, positive to heal)
		
		"""
		
		character.hp += amount
		