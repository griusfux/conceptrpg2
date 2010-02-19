# $Id$

# Description: Handles player keyboard and joystick input from Blender
# Contributers: Mitchell Stokes

class BlenderInput():
	def __init__(self, sensor, dict):
		self.sensor = sensor
		self.dict = dict
		
	def CheckInput(self):
		raise AttributeError("Input.CheckInput() is abstract")
	
	def ParseInput(self, input):
		for key in self.dict.keys():
			if input == self.dict[key]:
				return key
				
		return None

class BlenderKeyboardInput(BlenderInput):
	def CheckInput(self):
		if not self.sensor.positive:
			return None
		
		val = []
		for event in self.sensor.events:
			if event[1] == 1 or 2:
				temp = self.ParseInput(event[0])
				
				if temp:
					val.append(temp)
					
		return val
		
class BlenderJoystickInput(BlenderInput):
	def CheckInput(self):
		if not self.sensor.positive:
			return None
			
		val = []
		for event in self.sensor.getButtonActiveList():
			temp = self.ParseInput(event)
			
			if temp:
				val.append(temp)
				
class BlenderInputSystem():
	def __init__(self, keyboard, kb_conf, joystick=None, js_conf=None):
		import GameKeys
	
		# Load the config file for the keyboard inputs
		conf = open(kb_conf)
		
		kb_dict = {}
		
		# Go through the config file and load up a dictionary
		# dict["key"] = GameKey
		for line in conf:
			# Semicolons are comments and we don't want to do
			# anything with empty lines.
			if line.startswith(";") or not line.strip():
				continue
			key = line.split('=')
			
			# If we have a bad line, ignore it and tell the user.
			try:
				kb_dict[key[0]] = getattr(GameKeys, key[1].strip())
			except IndexError:
				print("Invalid line ignored: %s" % line)
			
		# Be safe and close the config file now that we're done
		conf.close()
		
		self.BlenderKeyboardInput = BlenderKeyboardInput(keyboard, kb_dict)
		
		# The joystick input is optional, so check for it first
		if joystick:
			# Now, do the same as for the keyboard...
			conf = open(js_conf)
			
			js_dict = {}
			
			for line in conf:
				button = lie.split('=')
				js_dict[button[0]] = int(b[1])
				
			conf.close()
			
			self.BlenderJoystickInput = BlenderJoystickInput(joystick, js_dict)
		else:
			# No joystick support
			self.BlenderJoystickInput = None
			
	# Call this method to run the manager
	# It will poll inputs and return them
	def Run(self):
		input = self.BlenderKeyboardInput.CheckInput()
		
		if self.BlenderJoystickInput:
			input.extend(self.BlenderJoystickInput.CheckInput())

		return input