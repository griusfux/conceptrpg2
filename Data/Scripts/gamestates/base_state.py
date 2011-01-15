# $Id$

import pickle
import Scripts.packages as packages
import Scripts.character_logic as character_logic

# This is used to implement RPC like functionality
class RPC:
	def __init__(self, state, client, rdict):
		# Stash the client and state
		self.state = state
		self.client = client
	
		self.funcs = rdict

	def invoke(self, f, *args):
		if f not in self.funcs:
			raise ValueError(f+" is not a registered function.\nAvailable functions: "+
								", ".join([v[0].__name__ for k, v in self.funcs.items()]))
	
		p = []
		
		# Check the data types and convert to strings
		for i in range(len(args)):
			t = self.funcs[f][1][i]
			v = args[i]
			if t is float:
				v = "%.4f" % v
			elif t == "pickle":
				v = str(pickle.dumps(v, 0), "ascii")
			elif not isinstance(v, t):
				print("Function:", f, "\nArgs:", args)
				raise ValueError("Argument "+str(i)+" should have been of type "+t.__name__+" got "+v.__class__.__name__+" instead.")
			else:
				v = str(v)
				
			p.append(v)
		# Send out the command
		self.client.send(f+":"+"$".join(p))
		
	def parse_command(self, main, data, client=None):
		if not data:
			return

		# Grab the functions and arguments
		s = data.split(':')
		if len(s) != 2:
			print("Invalid command string", data)
			return

		f, args = s[0], s[1].split('$')
		
		# Make sure we have a function we know
		if f not in self.funcs:
			print("Unrecognized function", f, "for state", self.state.__class__.__name__)
			return
		
		# Make sure we have the correct number of arguments
		if len(self.funcs[f][1]) != 0 and len(args) != len(self.funcs[f][1]):
			print("Invalid command string (incorrect number of arguments)", data)
			return
		
		# Change the strings to the correct data types
		for i in range(len(self.funcs[f][1])):
			t = self.funcs[f][1][i]
			
			if t == "pickle":
				args[i] = pickle.loads(bytes(args[i].replace(' ', '\n'), "ascii"))
			else:
				args[i] = t(args[i])
		
		if client:
			if len(self.funcs[f][1]) != 0:
				self.funcs[f][0](self.state, main, client, *args)
			else:
				self.funcs[f][0](self.state, main, client)
		else:
			if len(self.funcs[f][1]) != 0:
				self.funcs[f][0](self.state, main, *args)
			else:
				self.funcs[f][0](self.state, main)
		

# This class shouldn't be used directly, but rather subclassed

class BaseState:
	"""Base gamestate"""
	
	def __init__(self, main, is_server=False):
		"""BaseState Constructor"""
		
		# Store main
		self.main = main
		
		# This variable allows for switching states without a return (used for RPC functions)
		self._next_state = ""
		
		# Merge function dicts
		if hasattr(self, "client_functions") and type(self) is not BaseState:
			d = self.client_functions
			self.client_functions = BaseState.client_functions.copy()
			self.client_functions.update(d)
		if hasattr(self, "server_functions") and type(self) is not BaseState:
			d = self.server_functions
			self.server_functions = BaseState.server_functions.copy()
			self.server_functions.update(d)

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
		if self._next_state: return (self._next_state, "SWITCH")
	
		# Update main
		self.main = main
		
		# Run the appropriate method
		if self._is_server:
			self.client = RPC(self, client, self.client_functions)
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
		
	# At this level, we just ignore disconnects
	def dis(self, main, id):
		pass
		
	def move(self, main, cid, x, y, z):
		pass
		
	def rotate(self, main, cid, x, y, z):
		pass
		
	def position(self, main, cid, x, y, z):
		pass
		
	def add_player(self, main, id, race, pos, ori):
		if id in main['net_players']:
			# This player is already in the list, so just ignore this call
			return
	
		race = packages.Race(race)
		main['engine'].load_library(race)
		
		obj = main['engine'].add_object(race.root_object, pos, ori)
		main['net_players'][id] = character_logic.PlayerLogic(obj)
	
	# Register the functions
	client_functions = {
			"cid": (cid, (str,)),
			"to": (to, (str,)),
			"dis": (dis, (str,)),
			"move": (move, (str, float, float, float)),
			"rotate": (rotate, (str, float, float, float)),
			"position": (position, (str, float, float, float)),
			"add_player": (add_player, (str, str, "pickle", "pickle")),
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
	def dis(self, main, client):
		client.server.broadcast("dis:"+client.id)
		client.server.drop_client(client.peer, "Disconnected")
		
	def add_player(self, main, client, race, pos, ori):
		client.server.add_player(client.id, race, pos, ori)
		self.clients.invoke('add_player', client.id, race, pos, ori)
		
		for k, v in main['players'].items():
			self.client.invoke('add_player', k, v.race, v.position, v.orientation)
		
	def switch_state(self, main, client, state):
		self._next_state = state
		
	# Register the functions
	server_functions = {
			"dis": (dis, ()),
			"add_player": (add_player, (str, "pickle", "pickle")),
			"switch_state": (switch_state, (str,)),
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
		