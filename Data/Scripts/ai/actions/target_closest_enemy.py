import cego
from cego.actions._action import *
from cego.lib.euclid import Vector3

from Scripts.packages import Power

class target_closest_enemy(action):
	def __call__(self):
		
		target_count = self.args[0] if len(self.args) > 0 else 1
		
		cont = cego.manager.get_controller()
		targets = cont.get_targets_ex(self.agent, 'ALL', 0)
		
		targets.sort(key=lambda target: (Vector3(*target.position)-Vector3(*self.agent.position)).magnitude_squared())
		
		self.agent.targets = targets[:target_count]