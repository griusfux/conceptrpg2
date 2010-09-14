class Manager:
	def __init__(self, game_state):
		self.game_state = game_state
		self.agents = game_state.monster_list
		
	def run(self):
		for agent in self.agents:
			for action in agent.actions:
				action = getattr(__import__("Scripts.ai.actions." + action, fromlist=[action]), action)
				action(self.game_state, agent)