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
			2000,
			3000,
			4000,]
			
BASE_AFFINITIES = {
				# Elemental Affinities
				"death" : 0,
				"storm" : 0,
				"fire" : 0,
				"holy" : 0,
				"earth" : 0,
				"water" : 0,
				
				# Delivery Affinities
				"weapon" : 0,
				"spell" : 0
			}

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
		self.race		= None
		self.player_class= None
		self.element    = "Death"
		self.affinities = BASE_AFFINITIES.copy()
		self._xp			= 0
		self.last_level = 0
		self.next_level = 0
		self.affinity_points = 0
		self.delivery_points = 0
		self.power_points = 0
		
		#attributes
		self.endurance		= 5
		self.arcane_damage	= 5
		self.arcane_defense = 5
		self.physical_damage= 5
		self.physical_defense=5
		self.accuracy		= 5
		self.reflex			= 5
							
		#hit points
		self.max_hp		= 0
		self.hp			= 0
		
		#speed
		self.speed		= 5
		
		#inventory and equipment
		self.inventory = []
		self._armor	= self.Dummy()
		self._shield = self.Dummy()
		self._weapon = self.Dummy()
		self.credits	= 100
		
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
		self.max_hp = self.endurance * 5
		hp_percent = (self.hp / self.max_hp) if self.max_hp else 1
		self.hp = self.max_hp * hp_percent
		
		
	def apply_affinities(self):
		for k, v in self.player_class.affinities.items():
			self.affinities[k] += v
			
		# Still need to apply affinities based on element

	def level_up(self):
		self.level += 1
		
		if self.level == 1:
			self.power_points += 3
			self.apply_affinities()
		elif self.level % 5:
			self.affinity_points += 1
			self.power_points += 1
			self.delivery_points += 1
			self.apply_affinities()
		else:
			self.affinity_points += 1
			self.power_points += 1

	# Managed access to xp
	@property
	def xp(self): return self._xp
	
	@xp.setter
	def xp(self, value):
		self._xp = value
		
		while self.level < len(XP_TABLE) and self._xp >= self.next_level:
			self.level_up()
			self.last_level = self.next_level
			if self.level < len(XP_TABLE):
				self.next_level = XP_TABLE[self.level]
			else:
				print("Level cap reached")
			self.recalc_stats()
			
			# Debug prints
#			print(self.affinities)
#			print(self.affinity_points)
#			print(self.power_points)
#			print(self.delivery_points)

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
			
	def get_info(self):
		info = {
				"name"	: self.name,
				"level"	: self.level,
				"race"	: self.race.package_name,
				"player_class" : self.player_class.package_name if self.player_class else None,
				"xp"		: self.xp,
				
				"endurance" : self.endurance,
				"arcane_damage" : self.arcane_damage,
				"arcane_defense" : self.arcane_defense,
				"physical_damage" : self.physical_damage,
				"physical_defense" : self.physical_defense,
				"reflex" : self.reflex,
				"accuracy" : self.accuracy,
				
				"affinities" : self.affinities,
				"power_points" : self.power_points,
				"affinity_points" : self.affinity_points,
				"delivery_points" : self.delivery_points,
				
				"speed" : self.speed,
				
				"inventory"	: self.inventory,
				"armor"		: self.armor if self.armor else None,
				"weapon"	: self.weapon if self.weapon else None,
				"shield"	: self.shield if self.shield else None,
				"credits"		: self.credits,
				
				"powers"	: [power.package_name for power in self.powers.all]
			}
		
		return info
	
	def load_from_info(self, info):
		self.name		= info["name"]
		self.level		= info["level"]
		self.race		= Race(info["race"])
		if info["player_class"]:
			self.player_class = Class(info["player_class"])
		self._xp			= info["xp"]
		
		self.endurance		= info["endurance"]
		self.arcane_damage	= info["arcane_damage"]
		self.arcane_defense = info["arcane_defense"]
		self.physical_damage = info["physical_damage"]
		self.physical_defense = info["physical_defense"]
		self.accuracy = info["accuracy"]
		self.reflex = info["reflex"]

		self.affinities = info["affinities"]
		self.power_points = info["power_points"]
		self.affinity_points = info["affinity_points"]
		self.delivery_points = info["delivery_points"]
		
		self.speed = info["speed"]
		
		self.inventory = info["inventory"]
		self.armor = info["armor"]
		self.weapon = info["weapon"]
		self.shield = info["shield"]
		self.credits 		= info["credits"]
		
		self.powers		= PowerManager(self, info["powers"])
		
		if self.level == 0:
			self.xp += 0
		self.next_level = XP_TABLE[self.level] if self.level < len(XP_TABLE) else XP_TABLE[-1]
		self.last_level = XP_TABLE[self.level-1]

		self.recalc_stats()
		
class PlayerLogic(CharacterLogic):		
	def load(self, save):
		"""Fills in stats from a SaveData object"""
		
		self.load_from_info(save.data)
		
		# We shouldn't let this happen
		if not self.player_class:
			raise RuntimeError("The loaded save state did not have a player class!")
		
	def save(self):
		save_data = self.get_info()
		
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
		
		self.xp_reward = 0
#		self.xp_reward = monsterdata.xp_reward
#		self.credit_reward = monsterdata.credit_reward
#		self.role = monsterdata.role
#		self.leader = False
#		self.elite	= False
#		self.object = object
#		self.behaviors = []
		
		self.name = monsterdata.name
		self.hp = 20
		# self.level = monsterdata.level
		# self.role = monsterdata.role
		# self.leader = monsterdata.leader
		# self.elite = monsterdata.elite
		
		# self.ai_keywords = monsterdata.ai_keywords
		# self.ai_start_state = monsterdata.ai_start_state

		# self.recalc_stats()
		