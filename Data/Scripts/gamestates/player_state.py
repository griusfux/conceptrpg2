from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class PlayerState(DefaultState):
	"""A state for player screens"""
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		main['camera'].target = main['player'].object
		main['camera'].change_mode("shop", 30)
		
#		self.last_layout = main['ui_system'].current_layout
		self.layout = ""
		
		main['player_exit'] = False
		main['player_old_powers'] = main['player'].powers.all[:]
		main['player_controller'] = self
		main['drop_item'] = None
	def client_run(self, main):
		"""Client-side run method"""
		player = main['player']
		
		# Update the camera (this allows it to be animated)
		main['camera'].update()
		
		# If the camera is still transitioning, wait
		if main['camera']._transition_point != 0:
			return
		
		# If the player window isn't up yet, put it up
		if not self.layout:
			if main['overlay'] == "PlayerStats":
				self.layout = "PlayerStatsLayout"
			elif main['overlay'] == "Inventory":
				self.layout = "InventoryLayout"
			elif main['overlay'] == "Powers":
				self.layout = "PowersLayout"
			main['ui_system'].add_overlay(self.layout)
			
		# Get inputs
		inputs = main['input_system'].run()

		if ("Character", "INPUT_CLICK") in inputs:
			if main['overlay'] == "PlayerStats":
				return('', "POP")
			main['overlay'] = "PlayerStats"
			return("Player", "SWITCH")

		if ("Powers", "INPUT_CLICK") in inputs:
			if main['overlay'] == "Powers":
				return('', "POP")
			main['overlay'] = "Powers"
			return("Player", "SWITCH")

		if ("Inventory", "INPUT_CLICK") in inputs:
			if main['overlay'] == "Inventory":
				return('', "POP")
			main['overlay'] = "Inventory"
			return("Player", "SWITCH")
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return('', 'POP')
		
		if main['drop_item']:
			item = main['drop_item']
			main['player'].inventory.remove(item)
			
			if item == player.armor:
				player.armor = None
			elif item == player.weapon:
				player.weapon = None
			elif item == player.shield:
				player.shield = None
			
			self.drop_item(item, player.position)
			main['drop_item'] = None
		
		if main['player_exit']:
			player.recalc_stats()
			player.save()
			return('', 'POP')
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		# If the user did not exit, make sure the powers get canceled
		if not main['player_exit'] and self.layout=="PowersLayout":
			main['ui_system'].overlays[self.layout].cancel()
		main['ui_system'].remove_overlay(self.layout)
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
		
		# Clean up main
		del main['player_exit']
		del main['player_old_powers']
		del main['player_controller']
