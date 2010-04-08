from Scripts.ValidateData import *

class MonsterData:
	"""A container for data from classfiles"""
	
	def __init__(self, datafile):
		
		self.allowed_roles = ('artillery', 'brute', 'controller', 'lurker', 'minion', 'skirmisher')
	
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "level":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "role":
				ValidateAllowedData(self, element.tag, element.text, self.allowed_roles)
			elif element.tag == "leader":
				ValidateBoolean(self, element.tag, element.text)
			elif element.tag == "elite":
				ValidateBoolean(self, element.tag, element.text)
			elif element.tag == "xp":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "str_ab":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "dex_ab":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "con_ab":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "int_ab":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "wis_ab":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "cha_ab":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "behaviors":
				self.behaviors = [getattr(__import__('Scripts.Ai.Behaviors.%s' % behavior, globals(), locals(), [behavior], -1), behavior) for behavior in element.text.split(', ')]