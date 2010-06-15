# $Id$

class PassiveCombatSystem:
	"""A combat system for when the player isn't actively engaged in an encounter"""
	
	def __init__(self):
		"""Constructor"""
		
		# Nothing to do right now
		pass
		
	def run(self, main):
		"""A high-level run method"""
		
		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].obj.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['3p_cam'])
		
		# Handles input
		inputs = main['input_system'].run()
		
		if inputs:
			if "SwitchCamera" in inputs:
				main['engine'].set_active_camera(main['top_down_camera'])
		
			self._move_player(main['player'], inputs)
			
	def _move_player(self, player, inputs):
		"""Move the player"""
		
		moving = False
		
		if "MoveForward" in inputs:
			player.obj.move((0, 5, 0), min=[None, 0, 0], max=[None, 50, 0])
			player.obj.play_animation("move")
			moving = True
		if "MoveBackward" in inputs:
			player.obj.move((0, -5, 0), min=[None, -50, 0], max=[None, 0, 0])
			player.obj.play_animation("move")
			moving = True
			
		if not moving:
			player.obj.play_animation("idle")
			player.obj.move((0, 0, 0))