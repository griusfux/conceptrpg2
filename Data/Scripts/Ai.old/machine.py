class Machine:
	def __init__(self, keywords, start_state='spawn'):
		self.states = {
					'spawn'	: spawn,
					'idle'	: idle,
					'target': target,
					'move'	: move,
					'act'	: act,
					'death'	: death,
					}
		self.current_state = start_state
		
		self.timer = 0
		self.counter = 0
		
		if keywords:
			for keyword in keywords:
				keyword = __import__("Scripts.Ai." + keyword, fromlist=[keyword.split('.')[1]])
				keyword.register(self)
			
	def run(self, input):
		self.current_state = self.states[self.current_state](self, input)

def spawn(self, input):
	return 'idle'
	
def idle(self, input):
	if input['self'].hp <= 0:
		return 'death'

	# Keep a list of states in the order to perform them
	next_state = ['target', 'move', 'act']
	
	# If we have gone past the length of the list, start back at 0
	if self.counter > len(next_state) - 1:
		self.counter = 0
	
	# Return the next state based on the counter, and increment the counter
	state =  next_state[self.counter]
	self.counter += 1
	return state
	
	
def target(self, input):
	self.target = None
	return 'idle'
	
def move(self, input):
	return 'idle'

def act(self, input):
	return 'idle'
	
def death(self, input):
	input['combat_system'].monster_list.remove(input['self'])
	input['self'].object.end()
	return 'idle'

if __name__ is "__main__":
	print("__name__ == '__main__'")
	machine = Machine(())
	while True:
		machine.run({})
