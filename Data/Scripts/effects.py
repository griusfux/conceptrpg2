import Scripts.packages as packages

class Effect:
	def __init__(self, id, effect_name, position, target=None, duration=0, delay=0, continuous=-1,
		collision=None):
		
		self.name = effect_name
		self.time = delay
		self.id = id
		
		self._object = None
		
		self._pos = position
		self._target = target
		self._duration = duration
		self._continuous = continuous
		
		# Save the delay incase the effect is recreated
		self._delay = delay
		
		# Store the functions for when the effect object is loaded
		# This is done manually in order to define a list of acceptable functions
		self._functions = {
							"collision" : collision,
							}
		
	def fire(self, engine):
		package = packages.Effect(self.name)
		engine.load_library(package)
		self._object = engine.add_object(package.name, self._pos)
		
		# XXX Direct object property access
		gameobj = self._object.gameobj
		gameobj["target"] = self._target
		gameobj["functions"] = self._functions
		
		if self._continuous > 0:
			return Effect(self.id, self.name, self._pos, self._target, self._duration,
							self._continuous, self._continuous, **self._functions)
		
		return None
		
		
class EffectSystem:
	def __init__(self, engine):
		self._engine = engine
		self._effects = []
		self._next_id = 0
		
	def create(self, effect_name, position, target=None, duration=0, delay=0, continuous=-1, **functions):
		effect = Effect(self._next_id, effect_name, position, target, duration, delay, continuous, **functions)
		self._effects.append(effect)
		self._next_id += 1
		return effect.id
		
	def remove(self, id):
		for effect in self._effects:
			if effect.id == id:
				self._effects.remove(effect)
		
	def update(self):
		for effect in self._effects:
			if effect.time == 0:
				result = effect.fire(self._engine)
				self.remove(effect.id)
				if result:
					self._effects.append(result)
			else:
				effect.time -= 1
			