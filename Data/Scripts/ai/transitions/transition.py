class transition:
	def __init__(self, agent, target_state):
		self.actions = []
		self.agent = agent
		self.target_state = target_state
		
	def triggered(self):
		return True