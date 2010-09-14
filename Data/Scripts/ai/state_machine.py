from Scripts.ai.base_state import BaseState

class StateMachine:
	def __init__(self, agent, state_list, initial_state = None):
		self.states = {}
		first = None
		
		for state in state_list:
			state_name = state[0]
			actions = state[1]
			entry_actions = state[2]
			exit_actions = state[3]
			transitions = state[4]
			new_state = BaseState(agent, actions, entry_actions, exit_actions, transitions)
			self.states[state_name] = new_state
			
			if first == None:
				first = new_state
		
		self.current_state = initial_state if initial_state else first
	
	def run(self):
		triggered_transition = None
		actions = []
		
		for transition in self.current_state.transitions:
			if transition.triggered():
				triggered_transition = transition
				break
		
		if triggered_transition:
			target_state = self.states[triggered_transition.target_state]
			
			actions += self.current_state.exit_actions
			actions += triggered_transition.actions
			actions += target_state.entry_actions
			
			self.current_state = target_state
			
			return actions
			
		else:
			return self.current_state.actions