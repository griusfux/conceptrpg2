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
			
def item_pickup(cont):
	main = gl.getCurrentScene().objects['DungeonEmpty']
	if 'player' not in main: return
	
	sens = cont.sensors['coll']
	
	if sens.positive:
		id = cont.owner['id']
		if sens.hitObject == main['player'].object.gameobj and \
				 id not in main['item_collisions'] and \
				 id in main['ground_items']:
			main['item_collisions'].append(id)

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
		own['actions'][actionset.name] = actionset.actions
		
		# Now load the library so it can be found by the engine
		own['engine'].load_library(actionset, type='Action')

	# Current room to use for the combat state
	own['room'] = None
	own['state_manager'] = GameStateManager("Title", own)
	own['init'] = True
	
	# Items that are on the ground
	own['ground_items'] = {}
	own['item_collisions'] = []
	
	own['net_players'] = {}
	
