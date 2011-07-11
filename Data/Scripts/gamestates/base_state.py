# $Id$

import pickle
import Scripts.packages as packages
import Scripts.character_logic as character_logic
import Scripts.effect_manager as effects

# This is used to implement RPC like functionality
def rpc(d, name, *args):
	def decorator(f):
		d[name] = (f, args)
		return f
	return decorator

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
				v = ("%.4f" % v).encode()
			elif t == "pickle":
				v = pickle.dumps(v, -1)
			elif not isinstance(v, t):
				print("Function:", f, "\nArgs:", args)
				raise ValueError("Argument "+str(i)+" should have been of type "+t.__name__+" got "+v.__class__.__name__+" instead.")
			else:
				v = str(v).encode()
				
			p.append(v)
		# Send out the command
		self.client.send(f.encode()+b":::"+b"$$".join(p))
		
	def parse_command(self, main, data, client=None):
		if not data:
			return

		# Grab the functions and arguments
		s = data.split(b':::')
		if len(s) != 2:
			print("Invalid command string", data)
			return

		f, args = s[0].decode(), s[1].split(b'$$')
		
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
				args[i] = pickle.loads(args[i])
			else:
				args[i] = t(args[i].decode())
		
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
	
	client_functions = {}
	server_functions = {}
	
	def __init__(self, main, is_server=False):
		"""BaseState Constructor"""
		
		# Store main
		self.main = main
		
		# This variable allows for switching states without a return (used for RPC functions)
		self._next_state = ""

		# Setup the Remote Procedure Calls
		c = main['server'] if is_server else main.get('client')
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
			val = main['client'].run() if "client" in main else None
			while val:
				self.clients.parse_command(main, val)
				val = main['client'].run()
			return self.client_run(main)
					
	##########
	# Client
	##########
	
	def _delete_player(self, main, cid):
		obj = main['net_players'][cid].object
		effect = effects.FadeEffect(obj, 25)
		def f_end(object, engine):
			object.end()
		effect.f_end = f_end
		self.add_effect(effect)
		
		del main['net_players'][cid]
	
	# Client functions
	@rpc(client_functions, "cid", str)
	def cid(self, main, id):
		print("Setting id to", id)
		main['client'].id = id
		
	@rpc(client_functions, "to", str)
	def to(self, main, cid):
		if 'net_players' not in main: return
		if id not in main['net_players']: return
		
		self._delete_player(self, main, cid)
		print(cid, "timed out.")
		
	@rpc(client_functions, "dis", str)
	def dis(self, main, cid):
		if 'net_players' not in main: return
		if id not in main['net_players']: return
		
		self._delete_player(self, main, cid)
		print(cid, "diconnected.")
		
	@rpc(client_functions, "remove_player", str)
	def remove_player(self, main, cid):
		"""Remove a player without printing a message"""
		if 'net_players' not in main: return
		if cid not in main['net_players']: return

		self._delete_player(main, cid)
		
	@rpc(client_functions, "move", str, float, float, float)
	def move(self, main, cid, x, y, z):
		pass
		
	@rpc(client_functions, "rotate", str, float, float, float)
	def rotate(self, main, cid, x, y, z):
		pass
		
	@rpc(client_functions, "position", str, float, float, float)
	def position(self, main, cid, x, y, z):
		pass
		
	@rpc(client_functions, "animate", str, str, int, int, int)
	def animate(self, main, cid, action, start, end, mode):
		if 'net_players' not in main: return
		if cid not in main['net_players']: return
		
		main['net_players'][cid].object.play_animation(action, start, end, mode=mode)

	@rpc(client_functions, "add_player", str, "pickle", int, "pickle", "pickle")
	def add_player(self, main, cid, char_info, is_monster, pos, ori):
		if cid in main['net_players']:
			# This player is already in the list, so just ignore this call
			return
	
		if is_monster != 0:
			race = packages.Monster(char_info)
		else:
			race = packages.Race(char_info['race'])
		main['engine'].load_library(race)
		
		if is_monster != 0:
			obj = main['engine'].add_object(race.name, pos, ori)
			main['net_players'][cid] = character_logic.MonsterLogic(obj, race)
		else:
			obj = main['engine'].add_object(race.root_object, pos, ori)
			obj.armature = obj
			main['net_players'][cid] = character_logic.PlayerLogic(obj)
			main['net_players'][cid].load_from_info(char_info)
		main['net_players'][cid].id = cid
	
	@rpc(client_functions, "drop_item", int, "pickle", float, float, float)
	def drop_item(self, main, id, item, x, y, z):
		obj = main['engine'].add_object("drop", [x, y, z])
		obj.gameobj['id'] = id
		main['ground_items'][id] = [item, obj]
		
	@rpc(client_functions, "pickup_item", "pickle")
	def pickup_item(self, main, item):
		print("You picked up this item:")
		print(item)
		
	@rpc(client_functions, "remove_item", int)
	def remove_item(self, main, id):
		if id not in main['ground_items']:
			return
		
		main['ground_items'][id][1].end()
		del main['ground_items'][id]
	
	def client_init(self, main):
		"""Initialize the client state"""
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
	@rpc(server_functions, "dis")
	def dis(self, main, client):
		client.server.broadcast(b"dis:::"+client.id.encode())
		client.server.drop_client(client.peer, "Disconnected")
		
	@rpc(server_functions, "add_player", "pickle", "pickle", "pickle")
	def add_player(self, main, client, char_info, pos, ori):
		client.server.add_player(client.id, char_info, pos, ori)
		self.clients.invoke('add_player', client.id, char_info, 0, pos, ori)
		
		for k, v in main['players'].items():
			self.client.invoke('add_player', k, v.char_info, 0, v.position, v.orientation)
		
	@rpc(server_functions, "animate", str, str, int, int, int)
	def s_animate(self, main, client, cid, action, start, end, mode):
		self.clients.invoke('animate', cid, action, start, end, mode) 
		
	@rpc(server_functions, "switch_state", str)
	def switch_state(self, main, client, state):
		self._next_state = state
		
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
		
	def add_effect(self, effect):
		id = self.main["effect_system"].add(effect)
		return id

# All states should have a controller interface by which things like the AI system may make use
# of the state. Subclass this controller and override methods as you need them.
class BaseController:
	"""Base controller interface"""
	
	def play_animation(self, character, animation, lock=0, mode=0):
		"""Instruct the character to play the animation
		
		character -- the charcter who will play the animation
		animation -- the animation to play
		lock -- how long to lock for the animation
		
		"""
		
		if lock:
			character.add_lock(lock)
		self.server.invoke("animate", character.id, animation['name'], animation['start'], animation['end'], mode)
		
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
				
	def modify_stat(self, character, stat, amount):
		if stat not in character.stat_mods:
			character.stat_mods[stat] = 0
		character.stat_mods[stat] += amount
		character.recalc_stats()
		