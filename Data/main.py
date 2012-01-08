# $Id: main.py 1087 2012-01-08 08:53:48Z Moguri $

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.blender_wrapper as BlenderWrapper
from Scripts.ui.blender_ui_system import *
from Scripts.effect_manager import EffectManager
from Scripts.packages import *
from Scripts.gamestate_manager import GameStateManager

from Scripts.blender_input_system import BlenderInputSystem
from Scripts.Engine.log import Log

import json
import os
import sys

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
		if 'player' in main and main['player']:
			main['player'].save()
			
		# Disconnect from the server
		if 'client' in main:
			main['client'].disconnect()

		# Close the server if we launched it
		if "server" in main:
			main['server'].terminate()
			del main['server']
			
		# Free any libraries
		# XXX This seems to cause some crashes right now. We really should get this fixed to clean up some memory.
#		if 'engine' in main:
#			main['engine'].free_libraries()
	except Exception as e:
		import traceback
		traceback.print_exc()
	
	gl.error = True
	
	# Close our log and return sys.stdout to the way it was
	sys.stdout.close()
	sys.stdout = sys.stdout.stream
	
	
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
			if 'map_source' in own:
				pass
#				own['map_data'] = own['map_source'].image
#				own['map_source'].refresh()
			# Update the ui
			if 'ui_system' in own:
				own['ui_system'].run(own)
			
			if 'init' not in own:
					init(own)
			elif own['init']:
				if own['profile_run']:
					import cProfile
					profiler = cProfile.Profile()
					profiler.runcall(own['state_manager'].run, own)
					profiler.dump_stats('stats2.profile')
					own['profile_run'] = False
				else:	
					own['state_manager'].run(own)
	
	except:
		import traceback
		traceback.print_exc()
		gl.error = True
		
def init(own):
	
	# Start logging
	sys.stderr = sys.stdout
	sys.stdout = Log(sys.stdout, open('log.txt', 'w'))
	print("Log start")
	
	own['profile_run'] = False
	
	# Create a wrapper for the engine
	if 'engine' not in own:
		own['engine'] = BlenderWrapper.Engine(own)
		
	# Store the message sensor used to detect combat
	own['encounter_message'] = own.sensors['encounter_mess']

	# Create a ui system
	if 'ui_system' not in own:
		own['ui_system'] = BlenderUISystem()
		scene = bge.logic.getCurrentScene()
		camera = scene.cameras['map_cam']
#		source = bge.texture.ImageRender(scene, camera)
#		source.alpha = True
#		source.background = [0,0,0,0]
		own['map_source'] = None #source
		own['map_data'] = None
		
	# Create an effect system
	if 'effect_system' not in own:
		own['effect_system'] = EffectManager(own['engine'])

	# Setup an input system
	own['input_system'] = BlenderInputSystem('keys.conf', 'mouse.conf')

	# Build the actions list
	print("\nLoading Actions . . .")
	own['actions'] = {}
	for actionset in ActionSet.get_package_list():
		if actionset.name not in own['actions']:
			own['actions'][actionset.name] = actionset.actions
			
			# Now load the library so it can be found by the engine
			own['engine'].load_library(actionset, type='Action')
		else:
			print("WARNING: Duplicate actionset found:", actionset.name)

	# Current room to use for the combat state
	own['room'] = None
	own['state_manager'] = GameStateManager("Title", own)
	own['init'] = True
	
	# Items that are on the ground
	own['ground_items'] = {}
	own['item_collisions'] = []
	
	# Used to determine any tutorials that need to be displayed
	own['tutorial_queue'] = []
	
	own['net_players'] = {}
	
