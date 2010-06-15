# $Id $

class InactiveCombatSystem:
	"""A combat system for when the player isn't actively engaged in an encounter"""
	
	def __init__(self):
		"""Constructor"""
		
		# Nothing to do right now
		pass
		
	def run(self, main):
		"""A high-level run method"""
		
		# Handles input
		inputs = main['input_system'].run()
		
		if inputs:
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
			player.obj.player_animation("idle")
			player.obj.move((0, 0, 0))