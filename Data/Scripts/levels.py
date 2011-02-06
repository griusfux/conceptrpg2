import Scripts.packages as packages

STR_INFO = "Strength measures your character's physical power. It's important for most characters who fight hand-to-hand."
CON_INFO = "Constitution represents your character's health, stamina, and vital force. All characters benefit from a high constitution score."
DEX_INFO = "Dexterity measures hand-eye coordination, agility, reflexes, and balance."
INT_INFO = "Intelligence describes how well your character learns and reasons."
WIS_INFO = "Wisdom measures your common sense, perception, self-discipline, and empathy. You use your wisdom score to notice details, sense danger, and get a read on other people."
CHA_INFO = "Charisma measures your force of personality"

class UnspentLevel:
	def __init__(self, level, player_class):
	
		############F####
		# Abililty points
		if level == 1:
			self.ability_points = 20
			self.ability_spend = "BUY"
		elif level in (4, 8, 14, 18, 24, 28):
			self.ability_points = 2
			self.ability_spend = "LIMIT_TWO"
		elif level in (11, 21):
			self.ability_points = 1
			self.abililty_spend = "ALL"
		else:
			self.ability_points = 0
			self.ability_spend = "NONE"
		
		#######
		# Feats
		if level % 2 == 0 or level in (1, 1, 21):
			self.feats = 1
		else:
			self.feats = 0
		
		########
		# Powers
		
		available_powers = [packages.Power(power) for power in player_class.powers]
		
		# Limit to current level and below
		available_powers = [power for power in available_powers if power.level <= level]
		
		
		# At wills
		self.at_will_powers = [power.name for power in available_powers if power.usage == 'AT_WILL']
		if level == 1:
			self.at_will_count = 2
		else:
			self.at_will_count = 0
			
		# Encounters
		self.encounter_powers = [power.name for power in available_powers if power.usage == 'ENCOUNTER']
		if level in (1, 3, 7):
			self.encounter_count = 1
		else:
			self.encounter_count = 0
			
		# Dailies
		self.daily_powers = [power.name for power in available_powers if power.usage == 'DAILY']
		if level in (1, 5, 9):
			self.daily_count = 1
		else:
			self.daily_count = 0
			
		self.level = level
		
		