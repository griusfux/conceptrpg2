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
		
		# At wills
		if level == 1:
			self.at_wills = 2
		else:
			self.at_wills = 0
			
		# Encounters
		if level in (1, 3, 7):
			self.encounters = 1
		else:
			self.encounters = 0
			
		# Dailies
		if level in (1, 5, 9):
			self.dailies = 1
		else:
			self.dailies = 0
		
		