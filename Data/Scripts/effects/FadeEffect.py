class FadeEffect:
	def __init__(self, object, duration=60, amount=-1):
		self.object = object
		self.time = duration
		self.amount = amount / duration
		
		self.f_end = None
		
	def _load(self, id, engine):
		self.id = id
		
	def _unload(self, engine):
		if self.f_end:
			self.f_end(self.object, engine)
		
	def _update(self, engine):
		if self.object.valid:
			color = self.object.color
			color[3] += self.amount
			self.object.color = color

	def _fire(self, engine):
		pass
