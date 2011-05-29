# $Id$

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.blender_wrapper as BlenderWrapper
from Scripts.ui.blender_ui_system import *
from Scripts.effect_manager import EffectManager
from Scripts.packages import *
from Scripts.gamestate_manager import GameStateManager

from Scripts.blender_input_system import BlenderInputSystem

import json
import os

# Create a shorthand for gl
import bge
gl = bge.logic

# Error handling global
gl.error = False
	
def animation(cont):
	mess = cont.sensors['mess']

	if mess.positive:
		if mess.bodies[0] in cont.actuators:
			cont.activate(mess.bodies[0])
		else:
			print("WARNING: No actuator found for animation: %s" % mess.bodies[0])

def exit_game(main):
	print("Exiting...")
	
	# We use try/except so that we always reach gl.endGame()
	try:
		# Attempt to save the player
		if 'player' in main:
			main['player'].save()
			
		# Disconnect from the server
		if 'client' in main:
			main['client'].disconnect()

		# Close the server if we launched it
		if "server" in main:
			main['server'].terminate()
			del main['server']
	except Exception as e:
		print(e)
	
	gl.error = True
	if main['exit'] == "RESTART":
		gl.restartGame()
	else:
		gl.endGame()
					
def in_game(cont):
	# Wrap this whole thing in a try/except to prevent console spam
	try:
		if gl.error:
			return
	
		own = cont.owner
		
		# Check for and handle exits
		#if cont.sensors['exit'].positive or 'exit' in own:
		if 'exit' in own:
			exit_game(own)
		else:
			# Update the ui
			if 'ui_system' in own:
				own['ui_system'].run(own)
			
			if 'init' not in own:
					init(own)
			elif own['init']:
				own['state_manager'].run(own)
	
	except:
		import traceback
		traceback.print_exc()
		gl.error = True
		
def init(own):
	# Create a wrapper for the engine
	if 'engine' not in own:
		own['engine'] = BlenderWrapper.Engine(own)

	# Create a ui system
	if 'ui_system' not in own:
		own['ui_system'] = BlenderUISystem()
		
	# Create an effect system
	if 'effect_system' not in own:
		own['effect_system'] = EffectManager(own['engine'])

	# Setup an input system
	own['input_system'] = BlenderInputSystem('keys.conf', 'mouse.conf')

	# Build the actions list
	print("\nLoading Actions . . .")
	own['actions'] = {}
	for set in ActionSet.get_package_list():
		for action in set.action_set:
			if action['name'] in own['actions']:
				print("\nERROR: An action with the name %s already exists!\n" % action.name)
				continue
			# Load the action into the dictionary
			own['actions'][action['name']] = {"name" : action['name'], "start" : action['start'], "end" : action['end']}
		# Now load the library so it can be found by the engine
		gl.LibLoad(set.name, "Action", set.blend)
	print()

	# Load default actions		
	own['default_actions'] = {}
	defaults_path = os.getcwd() + "/Actions/.config/"
	for file in os.listdir(defaults_path):
		if file.startswith("."):
			continue
			
		actions = json.load(open(defaults_path+file))
		for action in actions:
			if action in own['default_actions']:
				print("\nERROR: A default action with the name %s already exists!\n" % action)
				continue
			own['default_actions'][action] = own['actions'][actions[action]]	

	# Current room to use for the combat state
	own['room'] = None
	own['state_manager'] = GameStateManager("Title", own)
	own['init'] = True
	
	own['net_players'] = {}
	
