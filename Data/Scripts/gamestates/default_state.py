# $Id$

from Scripts.character_logic import PlayerLogic
from .base_state import BaseState, BaseController

class DefaultState(BaseState, BaseController):
	"""The default state for the game"""
	
	def __init__(self, main, is_server=False):
		"""DefaultState Constructor"""
		
		BaseState.__init__(self, main, is_server)
			
	##########
	# Client
	##########
			
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("default_state")
		
	def client_run(self, main):
		"""Client-side run method"""
		
		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].object.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['3p_cam'])
		
		print("Still safe")
		
		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		# Keep our connection to the server alive
		val = main['client'].run()
		
		while val != None:
			cid, data = val
			
			# XXX This needs to be cleaned up
			if cid not in main['net_players']:
				main['net_players'][cid] = PlayerLogic(main['engine'].add_network_player("DarkKnightArm"))
				# root = main['engine'].add_object("NetEmpty")
				# player = main['engine'].add_object("DarkKnightArm")
				# player.gameobj.setParent(root.gameobj)
				# main['net_players'][cid] = PlayerLogic(root)
			
			# Parse the inputs from the server
			try:
				for input in data:
					if input.startswith('mov'):
						input = input.replace('mov', '')
						main['net_players'][cid].object.move([float(i) for i in input.split('$')], min=[-50, -50, 0], max=[50, 50, 0])
					elif input.startswith('pos'):
						input = input.replace('pos', '')
						server_pos = [float(i) for i in input.split('$')]
						client_pos = main['net_players'][cid].object.position
						
						for i in range(3):
							if abs(server_pos[i]-client_pos[i]) > 1.0:
								client_pos[i] = server_pos[i]
							
						main['net_players'][cid].object.position = client_pos
					elif input.startswith('anim'):
						input = input.replace('anim', '')
						main['net_players'][cid].object.move((0, 0, 0))
						main['net_players'][cid].object.play_animation(input)
					elif input.startswith('to'):
						main['net_players'][cid].object.end()
						del main['net_players'][cid]
						print(cid, "timed out")
					elif input.startswith('dis'):
						main['net_players'][cid].object.end()
						del main['net_players'][cid]
						print(cid, "disconnected")
			except ValueError as e:
				print(e)
				print(val)
					
			val = main['client'].run()
			
		# The message we will send to the server
		pos = main['player'].object.position
		msg = "pos%.4f$%.4f$%.4f " % (pos[0], pos[1], pos[2])
		
		if inputs:
			if ("SwitchCamera", "INPUT_ACTIVE") in inputs:
				main['engine'].set_active_camera(main['top_down_camera'])
				
			if ("Stats", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("stats")				
				
			if ("Inventory", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("inventory_overlay")
		
			# Only let the player do stuff while they are not "locked"
			if not main['player'].lock:
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].powers.active.use(self, main['player'])
				if ("NextPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_next_active()
				if ("PrevPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_prev_active()

				if ("MoveForward", "INPUT_ACTIVE") in inputs:
					msg += "mov0$5$0 "
				if ("MoveBackward", "INPUT_ACTIVE") in inputs:
					msg += "mov0$-5$0 "
				if ("MoveRight", "INPUT_ACTIVE") in inputs:
					msg += "mov5$0$0 "
				if ("MoveLeft", "INPUT_ACTIVE") in inputs:
					msg += "mov-5$0$0 "
					
				if 'mov' not in msg:
					msg += "mov0$0$0"
					# self.play_animation(None, "idle")
				# else:
					# self.play_animation(None, "move")
	
		# Send the message
		main['client'].send(msg.strip())
		
		# Check to see if we need to move to the combat state
		# XXX This needs cleanup, we shouldn't be accessing KX_GameObject attributes
		if main.sensors['encounter_mess'].positive:
			import Scripts.blender_wrapper as Blender
			room = main['dgen'].rooms[main.sensors['encounter_mess'].bodies[0]]
			del room['encounter']
			main['room'] = Blender.Object(room)
			main['client'].send('stateCombat')
			return ('Combat', 'SWITCH')
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
		"""Server-side run method"""

		# Here we just need to broadcast the data to the other clients
		client.server.broadcast(client.id + " " + client.data)
		
		
		for input in client.data.split():
			if input.startswith("dis"):
				client.server.drop_client(client.id, "Disconnected")
			elif input.startswith("state"):
				input = input.replace('state', '')
				return (input, 'SWITCH')
		
	##########
	# Other
	##########
	
	# Empty ---
	
	##########
	# Controller
	##########
	
	def play_animation(self, character, animation, lock=0):
		"""Instruct the character to play the animation
		
		character -- the charcter who will play the animation
		animation -- the animation to play
		lock -- how long to lock for the animation
		
		"""
		
		character.add_lock(lock)
		self.main['client'].send('anim'+animation) # XXX should be done based on the supplied character
		
	def get_targets(self, type, range):
		"""Get targets in a range
		
		type -- the type of area (line, burst, etc)
		range -- the range to grab (integer)
		
		"""
		
		return []
