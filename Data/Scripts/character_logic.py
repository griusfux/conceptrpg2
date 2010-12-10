# $Id$

# Description: Handles character logic such as movement and stats
# Contributers: Daniel Stokes, Mitchell Stokes

import pickle
import random
import time

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
		self.paragon_path= ""
		self.epic_destiny= ""
		self._xp			= 0
		self.size		= ""
		self.alignment	= ""
		
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
		
		#initiative
		self.initiative			= 0
		self.initiative_buff	= 0
		
		#hit points
		self.max_hp		= 0
		self.bloodied	= 0
		self.surge_value= 0
		self.surges_day	= 0
		self.hp			= 0
		self.surges		= 0
		self.second_wind= False
		self.death_throw_fails = 0
		self.resistances= {}
		self.saving_throw_mods = {}
		self.conditions = []
		
		#speed
		self.speed		= 5
		self.speed_base = 0
		self.speed_armor_penalty = 0
		self.speed_item_mod	= 0
		self.speed_misc_mod	= 0
		
		#senses
		#skills
		
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
		
		#intiative
		self.initiative = self.dex_mod + self.level//2 + self.initiative_buff
		
		#hit points
		# if isinstance(self, PlayerLogic):
			# self.max_hp = int(self.player_class.hp_first_level) + (self.level - 1) * int(self.player_class.hp_per_level)
		self.max_hp = 12
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
		
		if self._xp >= 100:
			self.level += self._xp // 100
			self._xp = self._xp % 100
	
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
		
	def save_against(self, roll, defense, type=None):
		"""Checks to see if a player saves against a roll of optional type with the specified defense"""
		mod = 0
		if type in self.saving_throw_mods:
			mod += saving_throw_mods[type]			
		return self.defense + mod > roll
	
	def roll_dice(self, dice):
		x, y = [int(i) for i in dice.split("d")]
		roll = 0
		
		for die in range(x):
			random.seed()
			roll += random.randint(1, y)
		return roll
		
	def move_to_point(self, target):
		"""Moves the character toward a given target at it's speed"""
		
		# Get the vector to  the target
		target_vector = self.object.get_local_vector_to(target)
		
		self.object.move((self.speed * target_vector[0], self.speed * target_vector[1], 0), mode=0)
		
	############## DEPRICATED ###############
	def equip_armor(self, armor):
		"""Changes stats to newly equipped armor and then recalculates stats"""
		self.armor = armor
		self.ac_bonus = armor.ac_bonus
		self.recalc_stats()
		
	def equip_shield(self, shield):
		"""Changes stats to newly equipped shield and then recalculates stats"""
		self.shield = shield
		self.recalc_stats()
		
	def equip_weapon(self, weapon):
		"""Changes stats to newly equipped weapon"""
		self.weapon = weapon
	##########################################
		
		
class PlayerLogic(CharacterLogic):
	
	def __init__(self, obj):
		CharacterLogic.__init__(self, obj)
		self.last_update = [(0, 0, 0), (1, 1, 1)]
		
	def load_stats(self, save):
		"""Fills in stats from a SaveData object"""
		try:
			save_data = pickle.load(save)
		except pickle.UnpicklingError:
			print("Invalid save file")
		
		self.name		= save_data["name"]
		self.level		= save_data["level"]
		self.race		= save_data["race"]
		self.player_class = save_data["player_class"]
		self.paragon_path = save_data["paragon_path"]
		self.epic_destiny = save_data["epic_destiny"]
		self.xp			= save_data["xp"]
		self.alignment	= save_data["alignment"]
		
		self.str_ab		= save_data["str_ab"]
		self.con_ab		= save_data["con_ab"]
		self.dex_ab		= save_data["dex_ab"]
		self.int_ab		= save_data["int_ab"]
		self.wis_ab		= save_data["wis_ab"]
		self.cha_ab		= save_data["cha_ab"]
		
		self.speed_base = save_data["speed_base"]
		
		if save_data["equipped_armor"]:
			self.equip_armor(save_data["equipped_armor"])
		if save_data["equipped_shield"]:
			self.equip_shield(save_data["equipped_shield"])
		if save_data["equipped_weapon"]:
			self.equip_weapon(save_data["equipped_weapon"])

		self.recalc_stats()
		
	def save_stats(self, save):
		save_data = {
				"name"	: self.name,
				"level"	: self.level,
				"race"	: self.race,
				"player_class" : self.player_class,
				"paragon_path" : self.paragon_path,
				"epic_destiny" : self.epic_destiny,
				"xp"		: self.xp,
				"alignment" : self.alignment,
				
				"str_ab"	: self.str_ab,
				"con_ab"	: self.con_ab,
				"dex_ab"	: self.dex_ab,
				"int_ab"	: self.int_ab,
				"wis_ab"	: self.wis_ab,
				"cha_ab"	: self.cha_ab,
				
				"speed_base" : self.speed_base,
				
				"equipped_armor"	: self.equipped_armor,
				"equipped_shield"	: self.equipped_shield,
				"equipped_weapon" 	: self.equipped_weapon}
		pickle.dump(save_data, save)
		
	
class MonsterLogic(CharacterLogic):
	def __init__(self, object, monsterdata):
		CharacterLogic.__init__(self, object)
		# self.id = monsterdata.id

		self.target = None
		
		self.role = ""
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
		
	def __del__(self):
		if self.object:
			self.object.end()
		