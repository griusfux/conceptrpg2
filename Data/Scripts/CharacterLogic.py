# $Id$

# Description: Handles character logic such as movement and stats
# Contributers: Daniel Stokes, Mitchell Stokes

from Scripts.InventoryLogic import *
import pickle
import random
import time

class CharacterLogic:
	"""A logic object that stores all the information and methods of the player"""
	
	def __init__(self, obj):	
		#Player information
		self.name		= ""
		self.level		= 0
		self.player_class= ""
		self.paragon_path= ""
		self.epic_destiny= ""
		self.xp			= 0
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
		self.speed		= 0
		self.speed_base = 0
		self.speed_armor_penalty = 0
		self.speed_item_mod	= 0
		self.speed_misc_mod	= 0
		
		#senses
		#skills
		
		#equipment
		self.equipped_armor	= None
		self.equipped_shield = None
		self.equipped_weapon = None
		
		# the character's game object
		self.obj = obj
		
	def RecalcStats(self):
		"""Recalculates the player's stats that are calculated based on other stats"""
		#ability modifiers
		self.str_mod = -5 + self.str_ab // 2
		self.con_mod = -5 + self.con_ab // 2
		self.dex_mod = -5 + self.dex_ab // 2
		self.int_mod = -5 + self.int_ab // 2
		self.wis_mod = -5 + self.wis_ab // 2
		self.cha_mod = -5 + self.cha_ab // 2
		
		#defenses
		self.ac	= 10 + self.level//2 + self.ac_bonus + self.shield_bonus + self.ac_buff
		if self.equipped_armor == None or self.equipped_armor.type == "light":
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
		self.max_hp		= int(self.player_class.hp_first_level) + (self.level - 1) * int(self.player_class.hp_per_level)
		self.bloodied	= self.max_hp // 2
		self.surge_value= self.max_hp // 4
		
		#speed
		self.speed = self.speed_base + self.speed_armor_penalty + self.speed_item_mod + self.speed_misc_mod
		
	def EquipArmor(self, armor):
		"""Changes stats to newly equipped armor and then recalculates stats"""
		self.equipped_armor = armor
		self.ac_bonus = armor.ac_bonus
		self.speed_armor_penalty = armor.speed
		self.RecalcStats()
		
	def EquipShield(self, shield):
		"""Changes stats to newly equipped shield and then recalculates stats"""
		self.equipped_shield = shield
		self.shield_bonus = shield.shield_bonus
		self.RecalcStats()
		
	def EquipWeapon(self, weapon):
		"""Changes stats to newly equipped weapon"""
		self.equipped_weapon = weapon
		
	def SaveAgainst(self, roll, defense, type=None):
		"""Checks to see if a player saves against a roll of optional type with the specified defense"""
		mod = 0
		if type in self.saving_throw_mods:
			mod += saving_throw_mods[type]			
		return self.defense + mod > roll
	
	def RollDice(self, dice):
		x, y = [int(i) for i in dice.split("d")]
		roll = 0
		
		for die in range(x):
			random.seed(time.time())
			roll += random.randint(1, y)
		return roll
		
class PlayerLogic(CharacterLogic):
	
	def __init__(self, obj):
		CharacterLogic.__init__(self, obj)
		self.inventory = InventoryLogic()
		
	def LoadStatsFromSave(self, save):
		"""Fills in stats from a SaveData object"""
		try:
			save_data = pickle.load(save)
		except pickle.UnpicklingError:
			print("Invalid save file")
		
		self.name		= save_data["name"]
		self.level		= save_data["level"]
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
		
		if save_data["equipped_armor"]:
			self.EquipArmor(save_data["equipped_armor"])
		if save_data["equipped_shield"]:
			self.EquipShield(save_data["equipped_shield"])
		#self.equipped_weapon = save_data["equipped_weapon"]

		self.RecalcStats()
		
	def SaveStatsToSave(self, save):
		save_data = {
				"name"	: self.name,
				"level"	: self.level,
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
				
				"equipped_armor"	: self.equipped_armor,
				"equipped_shield"	: self.equipped_shield,
				"equipped_weapon" : self.equipped_weapon }
		pickle.dump(save_data, save)
		
	def PlayerPlzMoveNowzKThxBai(self, cheezburger):
		"""Move the player"""
		
		if cheezburger:
			if "MoveForward" in cheezburger:
				self.obj.Move((0, 5, 0))
			if "MoveBackward" in cheezburger:
				self.obj.Move((0, -5, 0))
			if "TurnLeft" in cheezburger:
				self.obj.Rotate((0, 0, 0.04))
			if "TurnRight" in cheezburger:
				self.obj.Rotate((0, 0, -0.04))
		