# $Id$

from time import time

class DefaultState:
	"""A combat system for when the player isn't actively engaged in an encounter"""
	
	def __init__(self, main):
		"""Constructor"""
		
		main['ui_system'].load_layout("passive_combat")
		self.inventory_window_active = False
		
	def run(self, main):
		"""A high-level run method"""
		
		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].obj.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['3p_cam'])
		
		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		if inputs:
			if ("SwitchCamera", "INPUT_ACTIVE") in inputs:
				main['engine'].set_active_camera(main['top_down_camera'])
				
			if ("Inventory", "INPUT_CLICK") in inputs:
				if self.inventory_window_active:
					main['ui_system'].remove_overlay("inventory_overlay")
					self.inventory_window_active = False
				else:
					main['ui_system'].add_overlay("inventory_overlay")
					self.inventory_window_active = True
		
			# Only let the player do stuff while they are not "locked"
			if not main['player'].lock:
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].active_power.use(self, main['player'], target)
				self._move_player(main['player'], inputs)
				
	def play_animation(self, char, action):
		char.obj.play_animation(action)
			
	def _move_player(self, player, inputs):
		"""Move the player"""
		
		moving = False
		
		if ("MoveForward", "INPUT_ACTIVE") in inputs:
			player.obj.move((0, 5, 0), min=[None, 0, 0], max=[None, 50, 0])
			moving = True
		if ("MoveBackward", "INPUT_ACTIVE") in inputs:
			player.obj.move((0, -5, 0), min=[None, -50, 0], max=[None, 0, 0])
			moving = True
		if ("MoveRight", "INPUT_ACTIVE") in inputs:
			player.obj.move((5, 0, 0), min=[0, None, 0], max=[50, None, 0])
			moving = True
		if ("MoveLeft", "INPUT_ACTIVE") in inputs:
			player.obj.move((-5, 0, 0), min=[-50, None, 0], max=[0, None, 0])
			moving = True
			
		if moving:
			player.obj.play_animation("move")
		else:
			player.obj.play_animation("idle")
			player.obj.move((0, 0, 0))