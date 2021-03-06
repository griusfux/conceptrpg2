# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# $Id$

import math

from Scripts.packages import *
from Scripts.character_logic import PlayerLogic, ELEMENT_COLOR
from Scripts.power_manager import *
from Scripts.inventory import *
from .base_state import BaseState, BaseController
import Scripts.items as Items


class CharacterCreationState(BaseState, BaseController):
	"""A state that handles creating a new character"""
	
	##########
	# Client
	##########
	
	ui_layout = "CharGenLayout"
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['cgen_data'] = {}
		main['cgen_exit'] = False
		main['cgen_help'] = False
		
		# Setup the camera
		self.scene = main['engine'].add_object("char_gen", (0,0,0), (0,0,0))
		main['engine'].set_active_camera("char_gen_camera")
		
		# Some variables for viewing the character
		self.character = None
		self.weapon = None
		self.weaponobj = None
		self.race = None
		self.pclass = None
		self.element = ""
	def client_run(self, main):
		"""Client-side run method"""
		if self.suspended:
			return
		
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenu", "PUSH")
		
		if main['cgen_help']:
			self.display_tutorial(None, "Race", force=True)
			self.display_tutorial(None, "Class", force=True)
			self.display_tutorial(None, "Element", force=True)
			main['cgen_help'] = False
		
		# Display any queued tutorials (no default state running yet)
		if not self.suspended and main['tutorial_queue']:
			main['tutorial_string'] = main['tutorial_queue'].pop(0)
			return("Tutorial", "PUSH")
		
		if main['cgen_data']:
			if not self.race or self.race.name != main['cgen_data']['race'].name:
				self.race = main['cgen_data']['race']
				if self.character:
					self.character.end()
				main['engine'].load_library(self.race)
				self.character = main['engine'].add_object(self.race.root_object,
															(0.5,-1.7,1.3),
															(0,0,math.radians(180)))
				# Need this for animations to work
				self.character.armature = self.character
				# Need this to reload the weapon
				self.pclass = None
				# Need this to reapply accent color
				self.element = ""
				
			if not self.pclass or self.pclass.name != main['cgen_data']['class'].name:
				self.pclass = main['cgen_data']['class']
				if self.weaponobj:
					self.weaponobj.end()
				self.weapon = Weapon(self.pclass.starting_weapon)
				main['engine'].load_library(self.weapon)
				self.weaponobj = main['engine'].add_object(self.pclass.starting_weapon)			
				self.character.socket_fill('right_hand', self.weaponobj)
				
			if self.element != main['cgen_data']['element']:
				self.element = main['cgen_data']['element']
				self.character.accent = ELEMENT_COLOR[self.element]
				
			idle = main['actions'][self.race.action_set][PlayerLogic.get_action(self, "Idle")]
			for i, v in enumerate(idle):
				self.character.play_animation(v['name'], v['start'], v['end'], mode=1, layer=i)
				
		
		# Check for cgen end
		if main['cgen_exit']:
			
			if main['cgen_data']:
				player = PlayerLogic(None)
				
				# Set the player's name
				player.name = main['cgen_data']['name']
						
				# Set the player's race
				player.race = main['cgen_data']['race']
				
				# Set the player's class
				player_class = main['cgen_data']['class']
				player.player_class = player_class
				
				# Set the player's element
				player.element = main['cgen_data']['element']	
				
				# This levels the player to 1
				player.xp += 0
				
				
				player.max_hp = 16
				player.speed = 3.0
				
				# Now it is time to fill in the rest of the stats
				player.recalc_stats()
				
				# Give the player an attack power
				player.powers.add(Power('Attack'), self)
				
				# Give the player racial traits
				# This needs to be done after giving the player xp to ensure there
				# is already an unspent level for level 1
				if player.race.traits:
					traits = player.race.traits
					try:
						player.powers.add(Feat(traits), self)
					except PackageError:
						print("Unable to open up the file %s for %s's racial traits" % (traits, player.race.name))
				
				# Setup player inventory
				
				w = Items.Weapon(player_class.starting_weapon, 1)
				player.inventory.append(w)
				player.weapon = w
				
				
				a = Items.Armor(player_class.starting_armor, 1)
				player.inventory.append(a)
				player.armor = a
				
				player.new = True
				player.save()

			return("CharacterSelect", "SWITCH")
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		self.scene.end()
		
		if self.character:
			self.character.end()
		
		# We added these so we need to get rid of them too
		del main['cgen_data']
		del main['cgen_exit']
		del main['cgen_help']
			
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