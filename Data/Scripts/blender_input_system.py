# $Id$

# Description: Handles player keyboard and joystick input from Blender
# Contributers: Mitchell Stokes

import bge

# Dictionary to map Ketsji input states to generic ones
INPUT_STATE = {
		bge.logic.KX_INPUT_NONE: "INPUT_NONE",
		bge.logic.KX_INPUT_ACTIVE: "INPUT_ACTIVE",
		bge.logic.KX_INPUT_JUST_ACTIVATED: "INPUT_CLICK",
		bge.logic.KX_INPUT_JUST_RELEASED: "INPUT_RELEASE",
	}
			
	
# utility method for parsing config data
def parse_conf(file):

	# Load the config file for the input
	conf = open(file)
	
	dict = {}
	
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
			dict[key[0]] = getattr(bge.events, key[1].strip())
		except IndexError:
			print("Invalid line ignored: %s" % line)
		
	# Be safe and close the config file now that we're done
	conf.close()
	
	return dict

class BlenderInput():
	def __init__(self, sensor, dict):
		self.sensor = sensor
		self.dict = dict
		
	def check_input(self):
		raise AttributeError("Input.check_input() is abstract")
	
	def parse_input(self, input):
		for key in self.dict.keys():
			if input == self.dict[key]:
				return key
				
		return None

class BlenderKeyboardInput(BlenderInput):
	def check_input(self):
		
		val = []
		for key, value in self.sensor.events.items():
			if value != bge.logic.KX_INPUT_NONE:
				temp = self.parse_input(key)
				
				if temp:
					val.append((temp, INPUT_STATE[value]))
					
		return val
		
class BlenderMouseInput(BlenderInput):
	def check_input(self):
		val = []
		
		for event, value in self.sensor.events.items():
			if value != bge.logic.KX_INPUT_NONE:
				temp = self.parse_input(event)
				
				if temp:
					val.append((temp, INPUT_STATE[value]))
					
		return val
		
	@property
	def position(self):
		return self.sensor.position
		
	@position.setter
	def position(self, value):
		self.sensor.position = value
		
	def show(self, val):
		self.sensor.visible = val

class BlenderJoystickInput(BlenderInput):
	def check_input(self):
		if not self.sensor.positive:
			return None
			
		val = []
		for event in self.sensor.getButtonActiveList():
			temp = self.parse_input(event)
			
			if temp:
				val.append(temp)
				
class BlenderInputSystem():
	def __init__(self, kb_conf, mouse_conf, js_conf=None):
		# Setup the keyboard
		kb_dict = parse_conf(kb_conf)		
		
		self.keyboard = BlenderKeyboardInput(bge.logic.keyboard, kb_dict)
		
		# Setup the mouse
		m_dict = parse_conf(mouse_conf)
		
		self.mouse = BlenderMouseInput(bge.logic.mouse, m_dict)
		
		
		# # The joystick input is optional, so check for it first
		# if js_conf:
			# # Now, do the same as for the keyboard...
			# conf = open(js_conf)
			
			# js_dict = {}
			
			# for line in conf:
				# button = lie.split('=')
				# js_dict[button[0]] = int(b[1])
				
			# conf.close()
			
			# self.BlenderJoystickInput = BlenderJoystickInput(joystick, js_dict)
		# else:
			# # No joystick support
			# self.BlenderJoystickInput = None
			
		# Completely disable joystick for now
		self.joystick = None		
			
	# Call this method to run the manager
	# It will poll inputs and return them
	def run(self):
		input = self.keyboard.check_input()
		input.extend(self.mouse.check_input())
		
		if self.joystick:
			input.extend(self.joystick.check_input())

		return input