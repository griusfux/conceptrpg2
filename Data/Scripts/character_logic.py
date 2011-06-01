# $Id$

# Description: Handles character logic such as movement and stats
# Contributers: Daniel Stokes, Mitchell Stokes

import pickle
import random
import time

from Scripts.packages import *
from Scripts.power_manager import PowerManager
from Scripts.levels import UnspentLevel

XP_TABLE =	[0,
			1000,
			2250,
			3750,
			5500,]
			# 7500,
			# 10000,
			# 13000,
			# 16500,
			# 20500,]

class CharacterLogic:
	"""A logic object that stores all the information and methods of the player"""
	
	class Dummy:
		"""A dummy item to represent a null for an equipment slot"""
		def __init__(self):
			self.name = "None"
			self.type = "none"
			self.weight = self.ac = self.bonus = self.speed = 0
			
		def __bool__(self):
			return False
			
	def __init__(self, obj):
		# Set up weapon sockets
		if obj and obj.armature:
			self.armature = obj.armature
			
		self.id = -1
			
		#Player information
		self.name		= ""
		self.level		= 0
		self.race		= ""
		self.player_class= ""
		self.element    = "NEUTRAL"
		self._xp			= 0
		self.last_level = 0
		self.next_level = 0
		self.unspent_levels = []
		
		#affinities
		self.affinities = { "death" : 0,
							"storm" : 0,
							"fire" : 0,
							"holy" : 0,
							"earth" : 0,
							"water" : 0,
							"weapon" : 0,
							"spell" : 0
							}
							
		#hit points
		self.max_hp		= 0
		self.hp			= 0
		self.surges		= 0
		
		#speed
		self.speed		= 5
		
		#inventory and equipment
		self.inventory = []
		self._armor	= self.Dummy()
		self._shield = self.Dummy()
		self._weapon = self.Dummy()
		self.credits	= 0
		self.inventory_weight = 0
		
		# the character's game object
		self.object = obj
		
		# The character's current "lock", which is represented as the time at which the lock ends
		self.lock = None
		
		self.powers = PowerManager(self, [])
		
		self.targets = []
		
		self.stat_mods = {}
		
	def __del__(self):
		if self.object:
			self.object.end()

	def add_lock(self, duration):
		self.lock = time.time()+duration
		
	def update_lock(self):
		if self.lock and time.time() > self.lock:
			self.lock = None

	def recalc_stats(self):
		"""Recalculates the player's stats that are calculated based on other stats"""
		
		#hit points
		hp_percent = (self.hp / self.max_hp) if self.max_hp else 1
		self.hp = self.max_hp * hp_percent
	
	# Managed access to xp
	@property
	def xp(self): return self._xp
	
	@xp.setter
	def xp(self, value):
		self._xp = value
		
		# if self._xp >= 100:
			# self.level += self._xp // 100
			# self._xp = self._xp % 100
			# self.recalc_stats()
		
		while self.level < len(XP_TABLE) and self._xp >= self.next_level:
			self.level += 1
			self.unspent_levels.append(UnspentLevel(self.level, self.player_class))
			self.last_level = self.next_level
			if self.level < len(XP_TABLE):
				self.next_level = XP_TABLE[self.level]
			else:
				print("Level cap reached")
			self.recalc_stats()
	
	######################
	# Equipment properties
	
	@property
	def armor(self):
		return self._armor
	@armor.setter
	def armor(self, value):
		if value:
			self._armor = value
		else:
			self._armor = self.Dummy()
	
	@property
	def shield(self):
		return self._shield	
	@shield.setter
	def shield(self, value):
		if value:
			self._shield = value
		else:
			self._shield = self.Dummy()
	
	@property
	def weapon(self):
		return self._weapon
	@weapon.setter
	def weapon(self, value):
		if value:
			self._weapon = value
		else:
			self._weapon = self.Dummy()
			self._weapon.name = "Unarmed"
	
	#######################
	# Hand socket functions
	
	def set_left_hand(self, object):
		if self.armature:
			self.object.socket_fill("left_hand", object)
		else:
			print("WARNING: Character %s has no armature to contain sockets" % self.name)
			
	def clear_left_hand(self, object = None):
		if self.armature:
			self.object.socket_clear("left_hand", object)
		else:
			print("WARNING: Character %s has no armature to contain sockets" % self.name)
		
	def set_right_hand(self, object):
		if self.armature:
			self.object.socket_fill("right_hand", object)
		else:
			print("WARNING: Character %s has no armature to contain sockets" % self.name)
			
	def clear_right_hand(self, object = None):
		if self.armature:
			self.object.socket_clear("right_hand", object)
		else:
			print("WARNING: Character %s has no armature to contain sockets" % self.name)
		
class PlayerLogic(CharacterLogic):		
	def load(self, save):
		"""Fills in stats from a SaveData object"""
		
		save_data = save.data
		
		self.name		= save_data["name"]
		self.level		= save_data["level"]
		self.race		= Race(save_data["race"])
		self.player_class = Class(save_data["player_class"])
		self._xp			= save_data["xp"]
		self.unspent_levels = save_data["unspent_levels"]
		
		self.speed = save_data["speed"]
		
		self.inventory = save_data["inventory"]
		self.armor = save_data["armor"]
		self.weapon = save_data["weapon"]
		self.shield = save_data["shield"]
		self.credits 		= save_data["credits"]
		
		self.powers		= PowerManager(self, save_data["powers"])
		
		if self.level == 0:
			self.xp += 0
		self.next_level = XP_TABLE[self.level] if self.level < len(XP_TABLE) else XP_TABLE[-1]
		self.last_level = XP_TABLE[self.level-1]

		self.recalc_stats()
		
	def save(self):
		save_data = {
				"name"	: self.name,
				"level"	: self.level,
				"race"	: self.race.package_name,
				"player_class" : self.player_class.package_name,
				"xp"		: self.xp,
				"unspent_levels" : self.unspent_levels,
				
				"speed" : self.speed,
				
				"inventory"	: self.inventory,
				"armor"		: self.armor if self.armor else None,
				"weapon"	: self.weapon if self.weapon else None,
				"shield"	: self.shield if self.shield else None,
				"credits"		: self.credits,
				
				"powers"	: [power.package_name for power in self.powers.all]
			}
		
		if Save.exists(self.name):
			# We'll open and overwrite the old one
			save = Save(self.name)
		else:
			# Create a new savefile
			save = Save.create(self.name)
			
		save.data = save_data
		save.name = self.name
		save.write()		
	
class MonsterLogic(CharacterLogic):
	def __init__(self, object, monsterdata):
		CharacterLogic.__init__(self, object)
		# self.id = monsterdata.id
		
		self.xp_reward = monsterdata.xp_reward
		self.credit_reward = monsterdata.credit_reward
		self.role = monsterdata.role
		self.leader = False
		self.elite	= False
		self.object = object
		self.behaviors = []
		
		self.name = monsterdata.name
		self.hp = 20
		# self.level = monsterdata.level
		# self.role = monsterdata.role
		# self.leader = monsterdata.leader
		# self.elite = monsterdata.elite
		
		# self.ai_keywords = monsterdata.ai_keywords
		# self.ai_start_state = monsterdata.ai_start_state

		# self.recalc_stats()
		