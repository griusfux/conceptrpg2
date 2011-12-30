class FadeEffect:
	def __init__(self, target, duration=60, amount=-1):
		self.target = target
		self.object = target.object
		self.time = duration
		self.amount = amount / duration
		
		self.remote_id = None
		self.f_end = None
			
	@staticmethod
	def create_from_info(info, translate):
		
		if info['target'] in translate:
			target = translate[info['target']]
		else:
			return None
		
		effect = FadeEffect(target, info['duration'], info['amount'])
		
		return effect
			
	def get_info(self):
		info = {
				'type' : "FadeEffect",
				'target' : self.target.id,
				'duration' : self.time,
				'amount' : self.amount * self.time,
				}
		
		return info
		
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
