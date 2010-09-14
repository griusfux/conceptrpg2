class BaseState:
	def __init__(self, agent, actions = [], entry_actions = [], exit_actions = [], transitions=[]):
		self.agent = agent
		self.actions = actions
		self.entry_actions = entry_actions
		self.exit_actions = exit_actions
		self.transitions = []
		
		for transition in transitions:
			trigger = transition[0]
			target_state = transition[1]
			transition_init = getattr(__import__("Scripts.ai.transitions." + trigger, fromlist=[trigger]), trigger)
			self.transitions.append(transition_init(self.agent, target_state))