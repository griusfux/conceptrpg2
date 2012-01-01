import sys

import Scripts.effects as Effect

def push(self, controller, user):
	self.amount = int(self.amount)
	
	effect = "arcane_damage_" + ("down" if self.amount < 0 else "up")
	
	ori = user.orientation
	pos = user.position
	effect = Effect.StaticEffect(effect, user, ori, duration=60, continuous=90)
	self.id = controller.add_effect(effect)
	
	user.mods[self.name] += self.amount
	
def pop(self, controller, user):
	user.mods[self.name] -= self.amount
	
	controller.end_effect(self.id)