# Damage types
DT_ACID = 1
DT_COLD = 2
DT_FIRE = 4
DT_FORCE = 8
DT_LIGHTNING = 16
DT_NECROTIC = 32
DT_POISON = 64
DT_PSYCHIC = 128
DT_RADIANT = 256
DT_SONIC = 512

# Effect types
ET_CHARM = 1
ET_CONJURATION = 2
ET_FEAR = 4
ET_HEALING = 8
ET_ILLUSION = 16
ET_POISON = 32
ET_RELIABLE = 64
ET_SLEEP = 128
ET_STANCE = 256
ET_ZONE = 512
ET_TELEPORTATION = 1024
ET_POLYMORPH = 2048

# 

# class Powers:
	# name
	# desc
	
	# id
	# class
	# level
	# usage
	# cost
	# damage_type
	# power_source
	# is_trigger
	
	# implements
	# weapons
	
class Power:
	
	def __init__(self, powerdata):
		self.name = powerdata.name
		self.animation = powerdata.animation
		self._use = powerdata.method
		
	def use(self, combat_system, user, target):
		self._use(self, combat_system, user, target)