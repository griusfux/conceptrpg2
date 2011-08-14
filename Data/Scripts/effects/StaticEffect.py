import Scripts.packages as packages

class StaticEffect:
	def __init__(self, visual, position, duration=0, delay=0, continuous=-1):
		self.visual = visual
		self.position = position
		self.duration = duration
		self.delay = delay
		self.continuous = continuous
		self.obj = None
		self.fired = False
		
	def _load(self, id, engine):
		self.id = id
		self.time = self.delay
		
	def _unload(self, engine):
		engine.remove_object(self.obj)
		
	def _update(self, engine):
		pass
		
	def _fire(self, engine):
		if self.fired:
			if self.continuous >= 0:
				self._unload(engine)
				self.time = self.continuous
				self.fired = False
				return True
			return False
		engine.load_library(packages.Effect(self.visual))
		self.obj = engine.add_object(self.visual, self.position, time=0)
		
		self.time = self.duration
		self.fired = True
		return True
			
	