# $Id$

# This is used to implement RPC like functionality
class RPC:
	def __init__(self, state, client, rdict):
		# Stash the client and state
		self.state = state
		self.client = client
	
		self.funcs = {}
	
		# Re-arrange the dict
		for func, args in rdict.items():
			self.funcs[func.__name__] = (func, args)
		
	def invoke(self, f, *args):
		if f not in self.funcs:
			raise ValueError(f+" is not a registered function")
	
		p = []
		
		# Check the data types and convert to strings
		for i in range(len(args)):
			t = self.funcs[f][1][i]
			v = args[i]
			if not isinstance(v, t):
				print("Function:", f, "\nArgs:", args)
				raise ValueError("Argument "+str(i)+" should have been of type "+t.__name__+" got "+v.__class__.__name__+" instead.")
			elif t is float:
				v = "%.4f" % v
			else:
				v = str(v)
				
			p.append(v)
		# Send out the command
		self.client.send(f+":"+"$".join(p))
		
	def parse_command(self, main, data, client=None):
		if not data:
			return

		# if data.startswith("move"):
			# print(data)
		# Grab the functions and arguments
		s = data.split(':')
		if len(s) != 2:
			print("Invalid command string", data)
			return

		f, args = s[0], s[1].split('$')
		
		# Make sure we have a function we know
		if f not in self.funcs:
			print("Unrecognized function", f)
			return
		
		# Make sure we have the correct number of arguments
		if len(args) != len(self.funcs[f][1]):
			print("Invalid command string (incorrect number of arguments)", data)
			return
		
		# Change the strings to the correct data types
		for i in range(len(self.funcs[f][1])):
			t = self.funcs[f][1][i]
			
			if t is float:
				args[i] = float(args[i])
		
		if client:
			self.funcs[f][0](self.state, main, client, *args)
		else:
			self.funcs[f][0](self.state, main, *args)
		

# This class shouldn't be used directly, but rather subclassed

class BaseState:
	"""Base gamestate"""
	
	def __init__(self, main, is_server=False):
		"""BaseState Constructor"""
		
		# Store main
		self.main = main
		
		# Merge function dicts
		if hasattr(self, "client_functions") and type(self) is not BaseState:
			self.client_functions.update(BaseState.client_functions)
		if hasattr(self, "server_functions") and type(self) is not BaseState:
			self.server_functions.update(BaseState.server_functions)
		
		# Setup the Remote Procedure Calls
		c = main['server'] if is_server else main['client']
		self.clients = RPC(self, c, self.client_functions)
		self.server = RPC(self, c, self.server_functions)
		
		if is_server:
			self.server_init(main)
			self.cleanup = self.server_cleanup
		else:
			self.client_init(main)
			self.cleanup = self.client_cleanup
			
		self._is_server = is_server
		
	def run(self, main, client=None):
		# Update main
		self.main = main
		
		# Run the appropriate method
		if self._is_server:
			self.server.parse_command(main, client.data, client)
			return self.server_run(main, client)
		else:
			val = main['client'].run()
			while val:
				self.clients.parse_command(main, val)
				val = main['client'].run()
			return self.client_run(main)
					
	##########
	# Client
	##########
	
	# Client functions
	def cid(self, main, id):
		print("Setting id to", id)
		main['client'].id = id
		
	# At this level, we just ignore time outs
	def to(self, main, id):
		pass		
		
	# At this level, we just ignore time disconnects
	def dis(self, main, id):
		pass
	
	# Register the functions
	client_functions = {
			cid: (str,),
			to: (str,),
			dis: (str,)
			}
	
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
	
	# Server functions
	def dis(self, main, client, cid):
		client.server.broadcast("dis:"+cid)
		client.server.drop_client(cid, "Disconnected")
		
	# Register the functions
	server_functions = {
			dis: (str,)
			}
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
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
		