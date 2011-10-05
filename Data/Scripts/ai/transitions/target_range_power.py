import Scripts.mathutils as mathutils
from Scripts.packages import Power as Power

from cego.transitions._transition import *
from cego.lib.euclid import Vector3

class target_range_power(transition):	
	def triggered(self):
		if not self.agent.targets:
			return False
		if len(self.args) != 2:
			print("cEgo Error: target_range_power transition has an invalid number of arguments (2 required)")
			
		operator = self.args[0]
		power = Power(self.args[1])
		
		if not valid_operator(operator, COMPARISON):
			print("cEgo Error: target_range_power transition has an invalid operator (comparison required)")
			return False
		
		user_pos = Vector3(*self.agent.position)
		target_pos = Vector3(*self.agent.targets[0].position)
		range = (target_pos - user_pos).magnitude()
		
		range -= self.agent.size
		range -= self.agent.targets[0].size
		
		distance = power.distance if not "WEAPON_RANGE" in power.flags else 1

		return eval('%s %s %s' %(range, operator, power.distance))	