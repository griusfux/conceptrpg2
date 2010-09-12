class StateMachine:
	def __init__(self, agent, state_list, initial_state = None):
		self.states = []
		
		for state in state_list:
			module = __import__("Scripts.ai.states." + state[0], fromlist=["State"])
			self.states.append(module.State(state[1]))
		
		self.current_state = initial_state if initial_state else self.states[0]
	
	def run(self):
		triggered_transition = None
		actions = []
		
		for transition in self.current_state.transitions:
			if transition.triggered:
				triggered_transition = transition
				break
				
		if triggered_transition:
			target_state = triggered_transition.target_state
			
			actions += current_state.exit_actions
			actions += triggered_transition.actions
			actions += target_state.entry_actions
			
			self.current_state = target_state
			
			return actions
			
		else:
			return self.current_state.actions