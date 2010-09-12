from Scripts.ai.actions.seek import seek

class State:
	def __init__(self, transitions):
		self.actions = [seek]
		self.entry_actions = []
		self.exit_actions = []
		
		self.transitions = transitions