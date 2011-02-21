#Import all effects into this file for one stop access
from Scripts.effects import *

		
class EffectManager:
	def __init__(self, engine):
		self._engine = engine
		self._effects = []
		self._next_id = 0
		
	def add(self, effect):
		self._effects.append(effect)
		effect._load(self._next_id, self._engine)
		self._next_id += 1
		return effect.id
		
	def remove(self, id):
		for effect in self._effects:
			if effect.id == id:
				effect._unload(self._engine)
				self._effects.remove(effect)
		
	def update(self):
		for effect in self._effects:
			if effect.time <= 0:
				if not effect._fire(self._engine):
					self.remove(effect.id)
			else:
				effect._update(self._engine)
				effect.time -= 1
			