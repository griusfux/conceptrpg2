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
			5500,
			7500,
			10000,
			13000,
			16500,
			20500,]

class CharacterLogic:
	"""A logic object that stores all the information and methods of the player"""
	
	class Dummy:
		"""A dummy item to represent a null for an equipment slot"""
		def __init__(self):
			self.name = "null"
			self.type = "none"
			self.weight = self.ac = self.bonus = self.speed = 0
			
	def __init__(self, obj):
		# Set up weapon sockets
		if obj.armature:
			self.armature = obj.armature
			
		#Player information
		self.name		= ""
		self.level		= 0
		self.race		= ""
		self.player_class= ""
		self._xp			= 0
		self.last_level = 0
		self.next_level = 0
		self.unspent_levels = []
		self.size		= ""
		
		#ability scores
		self.str_ab		= 0
		self.str_mod	= 0
		self.con_ab		= 0
		self.con_mod	= 0
		self.dex_ab		= 0
		self.dex_mod	= 0
		self.int_ab		= 0
		self.int_mod	= 0
		self.wis_ab		= 0
		self.wis_mod	= 0
		self.cha_ab		= 0
		self.cha_mod	= 0
		
		#defenses
		self.ac			= 0
		self.ac_bonus	= 0
		self.shield_bonus= 0
		self.ac_buff	= 0
		self.fortitude	= 0
		self.fort_buff	= 0
		self.reflex		= 0
		self.reflex_buff= 0
		self.will		= 0
		self.will_buff	= 0
		
		#hit points
		self.max_hp		= 0
		self.bloodied	= 0
		self.surge_value= 0
		self.surges_day	= 0
		self.hp			= 0
		self.surges		= 0
		self.second_wind= False
		self.resistances= {}
		self.saving_throw_mods = {}
		
		#speed
		self.speed		= 5
		self.speed_base = 0
		self.speed_armor_penalty = 0
		self.speed_item_mod	= 0
		self.speed_misc_mod	= 0
		
		#inventory and equipment
		self.inventory = []
		self._armor	= self.Dummy()
		self._shield = self.Dummy()
		self._weapon = self.Dummy()
		self.gold	= 0
		self.inventory_weight = 0
		
		# the character's game object
		self.object = obj
		
		# The character's current "lock", which is represented as the time at which the lock ends
		self.lock = None
		
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
		#ability modifiers
		self.str_mod = -5 + self.str_ab // 2
		self.con_mod = -5 + self.con_ab // 2
		self.dex_mod = -5 + self.dex_ab // 2
		self.int_mod = -5 + self.int_ab // 2
		self.wis_mod = -5 + self.wis_ab // 2
		self.cha_mod = -5 + self.cha_ab // 2
		
		#defenses
		self.ac	= 10 + self.level//2 + self.armor.ac + self.shield.bonus + self.ac_buff
		if self.armor.type in ("light", "none"):
			self.ac	= self.ac + self.dex_mod if(self.dex_ab > self.int_ab) else self.int_mod
		self.fortitude = 10 + self.level//2 + self.fort_buff
		self.fortitude += self.str_mod if(self.str_ab > self.con_ab) else self.con_mod
		self.reflex	= 10 + self.level//2 + self.reflex_buff + self.shield_bonus
		self.reflex	+= self.dex_mod if(self.dex_ab > self.int_ab) else self.int_mod
		self.will	= 10 + self.level//2 + self.will_buff
		self.will	+= self.wis_mod if(self.wis_ab > self.cha_ab) else self.cha_mod
		
		#hit points
		hp_percent = (self.hp / self.max_hp) if self.max_hp else 1
		if self.player_class:
			if hasattr(self.player_class, "hp_per_level"):
				self.max_hp = int(self.player_class.hp_first_level) + (self.level - 1) * int(self.player_class.hp_per_level)
			else:
				self.max_hp = 6 + (self.level-1) * 3
		self.hp = self.max_hp * hp_percent
		self.bloodied	= self.max_hp // 2
		self.surge_value= self.max_hp // 4
		
		#speed
		self.speed = self.speed_base + self.armor.speed + self.speed_item_mod + self.speed_misc_mod
	
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
		self.ac -= self._armor.ac
		self.speed -= self._armor.speed
		self._armor = self.Dummy() if value == None else value
		self.ac += self._armor.ac
		self.speed += self._armor.speed
	
	@property
	def shield(self):
		return self._shield	
	@shield.setter
	def shield(self, value):
		self.ac -= self._shield.bonus
		self._shield = self.Dummy() if value == None else value
		self.ac += self._shield.bonus
	
	@property
	def weapon(self):
		if self._weapon.type == "none":
			self._weapon.type == "unarmed"
		return self._weapon
	@weapon.setter
	def weapon(self, value):
		self._weapon = self.Dummy() if value == None else value
	
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
		
		self.str_ab		= save_data["str_ab"]
		self.con_ab		= save_data["con_ab"]
		self.dex_ab		= save_data["dex_ab"]
		self.int_ab		= save_data["int_ab"]
		self.wis_ab		= save_data["wis_ab"]
		self.cha_ab		= save_data["cha_ab"]
		
		self.speed_base = save_data["speed_base"]
		
		self.inventory = save_data["inventory"]
		self.gold 		= save_data["gold"]
		
		self.powers		= PowerManager(save_data["powers"])

		self.recalc_stats()
		
	def save(self):
		save_data = {
				"name"	: self.name,
				"level"	: self.level,
				"race"	: self.race.package_name,
				"player_class" : self.player_class.package_name,
				"xp"		: self.xp,
				"unspent_levels" : self.unspent_levels,
				
				"str_ab"	: self.str_ab,
				"con_ab"	: self.con_ab,
				"dex_ab"	: self.dex_ab,
				"int_ab"	: self.int_ab,
				"wis_ab"	: self.wis_ab,
				"cha_ab"	: self.cha_ab,
				
				"speed_base" : self.speed_base,
				
				"inventory"	: self.inventory,
				"gold"		: self.gold,
				
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

		self.target = None
		
		self.xp_reward = monsterdata.xp_reward
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
		# self.str_ab = monsterdata.str_ab
		# self.con_ab = monsterdata.con_ab
		# self.int_ab = monsterdata.int_ab
		# self.wis_ab = monsterdata.wis_ab
		# self.cha_ab = monsterdata.cha_ab
		
		self.ai_keywords = monsterdata.ai_keywords
		self.ai_start_state = monsterdata.ai_start_state

		# self.recalc_stats()
		