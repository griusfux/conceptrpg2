class CharacterLogic:
	"""A logic object that stores all the information and methods of the player"""
	
	def __init__(self):	
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
		
	def LoadStatsFromSave(self, save):
		"""Fills in stats from a SaveData object"""
		self.name		= save.name
		self.level		= save.level
		self.player_class = save.player_class
		self.paragon_path = save.paragon_path
		self.epic_destiny = save.epic_destiny
		self.xp			= save.xp
		self.alignment	= save.alignment
		
		self.str_ab		= save.str_ab
		self.con_ab		= save.con_ab
		self.dex_ab		= save.dex_ab
		self.int_ab		= save.int_ab
		self.wis_ab		= save.wis_ab
		self.cha_ab		= save.cha_ab
	
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
		if self.equipped_armor == None or self.equipped_armor.type == "light":			#If player is wearing light or no armor, apply dex or int modifier to ac (whichever is greater)
			self.ac	+= self.dex_mod if(self.dex_ab > self.int_ab) else self.int_mod
		self.fortitude = 10 + self.level//2 + self.fort_buff
		self.fortitude += self.str_mod if(self.str_ab > self.con_ab) else self.con_mod
		self.reflex	= 10 + self.level//2 + self.reflex_buff + self.shield_bonus
		self.reflex	+= self.dex_mod if(self.dex_ab > self.int_ab) else self.int_mod
		self.will	= 10 + self.level//2 + self.will_buff
		self.will	+= self.wis_mod if(self.wis_ab > self.cha_ab) else self.cha_mod
		
		#intiative
		self.initiative = self.dex_mod + self.level//2 + self.initiative_buff
		
		#hit points
		self.max_hp		= int(self.player_class.hp_first_level) + self.level * int(self.player_class.hp_per_level)
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
		
	def SaveAgainst(self, roll, defense, type=None):
		"""Checks to see if a player saves against a roll of optional type with the specified defense"""
		mod = 0
		if type in self.saving_throw_mods:
			mod += saving_throw_mods[type]			
		return self.defense + mod > roll

#Test code#
# player = Character()
# player.RecalcStats()
# print(player.fortitude)
# print(player.SaveAgainst(4, "fortitude"))