import Scripts.Ai.machine as machine

type = "movement"	
required_inputs = ('self', 'foe_list')

def move_happy(self, input):
	###########################
	# Check for required inputs
	valid = True
	for required_input in required_inputs:
		if required_input not in input:
			print("Required input %s was not found in the state inputs!\nThis input is neccessary for %s" % (required_input, __name__))
			valid = False
	if not valid:
		return 'idle'
		
	happy = False
	for player in input['foe_list']:
		target_x, target_y, target_z = player.object.position
		self_x, self_y, self_z = input['self'].object.position
		range = (target_x - self_x)**2 + (target_y - self_y)**2
		if range < 25 :
			happy = True
			break
			
	if happy and self.timer > 30:
		input['self'].object.move((0,0,300), 1)
		self.timer = 0
	
	return 'idle'
def idle_happy(self, input):
	self.timer += 1
	return machine.idle(self, input)
	
	
states = {
			'move'	: move_happy,
			'idle'	: idle_happy
		}
def register(machine):
	for key, value in states.items():
		machine.states[key] = value