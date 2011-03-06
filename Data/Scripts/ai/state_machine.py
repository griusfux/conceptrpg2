from Scripts.ai.base_state import BaseState
import json

class StateMachine:
	def __init__(self, agent, definition, initial_state = None):
		self.states = {}
		first = None
		
		definition = json.load(open(definition, 'r'))
		
		for state in definition['states']:
			transitions = definition['global_transitions'] + state['transitions']
			state_name = state['name']
			
			actions = state['actions']
			entry_actions = state['entry_actions']
			exit_actions = state['exit_actions']
			
			new_state = BaseState(agent, actions, entry_actions, exit_actions, transitions)
			self.states[state_name] = new_state
			
			if first == None:
				first = new_state
		
		self.current_state = self.states[initial_state] if initial_state else first
	
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