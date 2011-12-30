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

ELEMENT_COLOR = {
				"DEATH" : [0.5255, 0.6039, 0.3569],
				"STORM" : [0.9451, 0.9451, 0.4863],
				"FIRE" : [1.0000, 0.4667, 0.1686],
				"HOLY" : [0.7882, 0.9020, 0.9373],
				"EARTH" : [0.6863, 0.3961, 0.0784],
				"WATER" : [0.0706, 0.7137, 0.9020],
				"NEUTRAL" : [0.5, 0.5 ,0.5],
				
				}
			
BASE_AFFINITIES = {
				# Elemental Affinities
				"DEATH" : 0,
				"STORM" : 0,
				"FIRE" : 0,
				"HOLY" : 0,
				"EARTH" : 0,
				"WATER" : 0,
				"NEUTRAL" : 0,
				
				# Delivery Affinities
				"WEAPON" : 0,
				"SPELL" : 0
			}

CALLBACKS = {
			"ATTACK" : {},
			}

MODS = {
		"Arcane Damage" : 0,
		"Physical Damage" : 0,
		"Accuracy" : 0,
		"Arcane Defense" : 0,
		"Physical Defense" : 0,
		"Reflex" : 0,
		}

class CharacterLogic:
	"""A logic object that stores all the information and methods of the player"""
	
	class Dummy:
		"""A dummy item to represent a null for an equipment slot"""
		def __init__(self):
			self.name = "None"
			self.type = "none"
			self.range = 1
			self.damage =1
			
			# Stats (could be for any item type)
			self.physical_damage = 0
			self.physical_defense = 0
			self.arcane_damage = 0
			self.arcane_defense = 0
			self.reflex = 0
			self.accuracy = 0
			
		def __bool__(self):
			return False
			
	def __init__(self, obj):
		# Set up weapon sockets
		if obj and obj.armature:
			self.armature = obj.armature
			
		self.id = -1
			
		#Player information
		self.name		= ""
		self.tutorials	= []
		self.level		= 0
		self.race		= None
		self.player_class= None
		self.element    = "DEATH"
		self.affinities = BASE_AFFINITIES.copy()
		self._xp			= 0
		self.last_level = 0
		self.next_level = 0
		self.affinity_points = 0
		self.delivery_points = 0
		self.power_pool_max = 0
		self.power_pool = 0
		
		#attributes
		self.arcane_damage	= 5
		self.arcane_defense = 5
		self.physical_damage= 5
		self.physical_defense=5
		self.accuracy		= 5
		self.reflex			= 5
		
		self.mods = MODS.copy()
							
		#hit points
		self.max_hp		= 1
		self.hp			= 1
		self.hp_per_level = 5
		
		#speed
		self.speed		= 5
		
		# Size for range checks
		self.size		= 0.5
		
		#inventory and equipment
		self.inventory = []
		self._armor	= self.Dummy()
		self._shield = self.Dummy()
		self._weapon = self.Dummy()
		self.credits	= 100
		
		# the character's game object
		self._object = obj
				
		# Various flags
		self.flags = set()
		
		# Flag to notify that we need to resend player data over the server
		self.network_update = False
		
		# The character's current "lock", which is represented as the time at which the lock ends
		self.lock = 0
		
		self.powers = PowerManager(self, [])
		self.stance = ""
		
		self.targets = []
		self.auto_target = None
		self.auto_power = None
		
		self.statuses = []
		
		self.action_set = None
		
		self.callbacks = CALLBACKS.copy()
		
		self.recalc_stats()
		
	def __str__(self):
		return self.name
		
	def __del__(self):
		if self.object:
			self.object.end()

	def add_lock(self, duration):
		self.lock = duration
		
	def update_lock(self):
		if self.lock > 0:
			self.lock -= 1
		else:
			self.lock = 0

	def recalc_stats(self):
		"""Recalculates the player's stats that are calculated based on other stats"""
		
		#hit points
		hp_percent = (self.hp / self.max_hp)
		self.max_hp = int(self.hp_per_level * (self.level+1+self.affinities['NEUTRAL'])) 
		self.hp = int(self.max_hp * hp_percent)
		
		#other stats
		self.physical_damage = max(1, 10+self.affinities['STORM'])
		self.physical_damage += self.mods['Physical Damage']
		
		self.physical_defense = max(1, 10+self.affinities['EARTH'])
		self.physical_defense += self.mods['Physical Defense']
		
		self.arcane_damage = max(1, 10+self.affinities['DEATH'])
		self.arcane_damage += self.mods['Arcane Damage']
		
		self.arcane_defense = max(1, 10+self.affinities['HOLY'])
		self.arcane_defense += self.mods['Arcane Defense']
		
		self.reflex = max(1, 10+self.affinities['WATER'])
		self.reflex += self.mods['Reflex']
		
		self.accuracy = max(1, 10+self.affinities['FIRE'])
		self.accuracy += self.mods['Accuracy']
		
		# Stats from items
		self.physical_defense += self.armor.physical_defense
		self.arcane_defense += self.armor.arcane_defense
		self.reflex += self.armor.reflex
		
		# Recalc power pool
		self.power_pool = self.power_pool_max
		for power in self.powers:
			self.power_pool -= power.cost(self.affinities)
			
		self.network_update = True
		
	def apply_affinities(self):
		for k, v in self.player_class.affinities.items():
			self.affinities[k] += v
			
		affinities = ("STORM",
					  "FIRE",
					  "HOLY",
					  "EARTH",
					  "WATER",
					  "DEATH")

		idx = affinities.index(self.element)
		
		def mod_affinity(i, val):
			i %= len(affinities)
			
			self.affinities[affinities[i]] += val
			
		mod_affinity(idx+0, 2)
		mod_affinity(idx+1, 1)
		mod_affinity(idx-1, 1)
		
		mod_affinity(idx+3, -2)
		mod_affinity(idx+2, -1)
		mod_affinity(idx-2, -1)
				
		
	def manage_statuses(self, controller):
		for status in self.statuses:
			status.use(controller, self)
			status.time -= 1
			if status.time <= 0:
				status.pop(controller, self)
				self.statuses.remove(status)
				
	def add_callback(self, name, type, callback):
		if type not in CALLBACKS:
			print("WARNING: %s is not a supported character callback. Supported callbacks are:"%type)
			for key in CALLBACKS:
				print(key)
			return
		# New callbacks over write old ones
		self.callbacks[type][name] = callback
		
	def remove_callback(self, name, type):
		if type not in CALLBACKS:
			print("WARNING: %s is not a supported character callback. Supported callbacks are:"%type)
			for key in CALLBACKS:
				print(key)
			return
		if name in self.callbacks[type]:
			del self.callbacks[type][name]
			
	def add_status(self, controller, status):
		for _status in self.statuses:
			if _status.name == status.name:
				self.remove_status(controller, _status)
				break
				
		status.push(controller, self)
		self.statuses.append(status)
		self.recalc_stats()
	
	def remove_status(self, controller, status_name):
		for status in self.statuses:
			if status.name == status_name:
				status.pop(controller, self)
				self.statuses.remove(status)
		self.recalc_stats()
	
	def level_up(self):
		self.level += 1
		
		if self.level == 1:
			self.power_pool_max += 3
			self.affinity_points += 2
			self.apply_affinities()
		elif self.level % 5:
			self.affinity_points += 1
			self.power_pool_max += 1
			self.delivery_points += 1
			self.apply_affinities()
		else:
			self.affinity_points += 1
			self.power_pool_max += 1

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
		self.recalc_stats()
	
	@property
	def shield(self):
		return self._shield	
	@shield.setter
	def shield(self, value):
		if value:
			self._shield = value
		else:
			self._shield = self.Dummy()
		self.recalc_stats()
	
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
		self.recalc_stats()
	
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
				"tutorials" : self.tutorials,
				"level"	: self.level,
				"race"	: self.race.package_name,
				"player_class" : self.player_class.package_name if self.player_class else None,
				"element"	: self.element,
				"xp"		: self.xp,

				"arcane_damage" : self.arcane_damage,
				"arcane_defense" : self.arcane_defense,
				"physical_damage" : self.physical_damage,
				"physical_defense" : self.physical_defense,
				"reflex" : self.reflex,
				"accuracy" : self.accuracy,
				
				"affinities" : self.affinities,
				"power_pool_max" : self.power_pool_max,
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
		self.tutorials	= info["tutorials"]
		self.level		= info["level"]
		if info["player_class"]:
			self.player_class = Class(info["player_class"])
		self.element		= info["element"]
		self._xp			= info["xp"]

		self.arcane_damage	= info["arcane_damage"]
		self.arcane_defense = info["arcane_defense"]
		self.physical_damage = info["physical_damage"]
		self.physical_defense = info["physical_defense"]
		self.accuracy = info["accuracy"]
		self.reflex = info["reflex"]

		self.affinities = info["affinities"]
		self.power_pool_max = info["power_pool_max"]
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
		self.last_level = XP_TABLE[self.level-1] if self.level-1 < len(XP_TABLE) else XP_TABLE[-1]
		
		self.recalc_stats()

	def get_action(self, action):
		return action
		
	@property
	def position(self):
		return self.object.position
	
	@position.setter
	def position(self, v):
		self.object.position = v
		
	@property
	def orientation(self):
		return self.object.get_orientation()
	
	@orientation.setter
	def orientation(self, v):
		self.object.orientation = v
		
	@property
	def object(self):
		return self._object
	
	@object.setter
	def object(self, obj):
		# Apply accent color
		if obj:
			obj.accent = ELEMENT_COLOR[self.element]
		self._object = obj
		
		
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
		
	def load_from_info(self, info):
		CharacterLogic.load_from_info(self, info)

		self.race		= Race(info["race"])
		if self.race:
			self.action_set = self.race.action_set
		
	def reset_weapon_mesh(self, engine):
		self.clear_right_hand()

		if self.weapon:
			obj = self.weapon.createObjectInstance(engine)
			self.set_right_hand(obj)
	
	def get_action(self, action):
		v = "Empty"
		
		if self.weapon:
			wtype = self.weapon.type
			whands = self.weapon.hands
	
			# 'SWORD', 'AXE', 'POLEARM', 'BLUNT', 'BOW', 'GUN', 'THROWN'
			if whands == 2:
				if wtype == "SWORD":
					v = "1h"
				elif wtype == "AXE":
					v = "1h"
				elif wtype == "POLEARM":
					v = "Spear"
				elif wtype == "BLUNT":
					v = "1h"
				elif wtype == "BOW":
					v = "Bow"
				elif wtype == "GUN":
					v = "1h"
				elif wtype == "THROWN":
					v = "1h"
			else: # One handed weapons
				if wtype == "SWORD":
					v = "1h"
				elif wtype == "AXE":
					v = "1h"
				elif wtype == "POLEARM":
					v = "1h"
				elif wtype == "BLUNT":
					v = "1h"
				elif wtype == "GUN":
					v = "1h"
				elif wtype == "THROWN":
					v = "1h"
			
			# If we made it this far without changing v, we've missed a case.
			if v == "Empty":
				print("WARNING Missing weapon animation case: Hands=%d, Type=%s" % (whands, wtype))
				v = "1h"
		return " ".join([action, v])

class MonsterLogic(CharacterLogic):
	def __init__(self, object, monsterdata, level=1):
		CharacterLogic.__init__(self, object)
		
		# For cego.Agent
		self.time = 0

		self.level = max(level+monsterdata.level_adjustment, 1)
		self.action_set = monsterdata.action_set
		
		self.xp_reward = monsterdata.xp_reward
		
		self.size = monsterdata.size
		self.speed = monsterdata.speed
		
		# Handle affinities
		if level > 1:
			totals = {}
			running_total = 0
			
			for k, v in monsterdata.affinities.items():
				weight = max(1, v+5)
				running_total += weight
				totals[k] = running_total
				self.affinities[k] = v
				
			for i in range(level-1):
				rnd = random.random()*running_total
				
				for k, v in totals.items():
					if rnd < v:
						self.affinities[k] += 1
						break
		
		self.name = monsterdata.name
		self.hp_per_level = monsterdata.hp_per_level
		self.element = monsterdata.element
		self.race = monsterdata
		
		self.recalc_stats()
		
	def load_from_info(self, info):
		CharacterLogic.load_from_info(self, info)
		
		self.race = Monster(info['race'])

		# self.recalc_stats()
		