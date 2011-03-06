class Manager:
	def __init__(self, game_state, agent_list):
		self.game_state = game_state
		self.agents = agent_list
		
	def run(self):
		for agent in self.agents:
			for action in agent.actions:
				action = getattr(__import__("Scripts.ai.actions." + action, fromlist=[action]), action)
				action(self.game_state, agent)
				
	def add_agent(self, agent):
		self.agents.append(agent)