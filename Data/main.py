# $Id$

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.blender_wrapper as BlenderWrapper
from Scripts.ui.blender_ui_system import *
from Scripts.effects import EffectSystem
from Scripts.packages import *
from Scripts.dungeon_generator import DungeonGenerator
from Scripts.character_logic import PlayerLogic, MonsterLogic
from Scripts.gamestate_manager import GameStateManager
from Scripts.power_manager import PowerManager
from Scripts.inventory import Inventory

from Scripts.blender_input_system import BlenderInputSystem

from Scripts.networking.game_client import GameClient

import subprocess
import pickle
import os
import json
import sys
import struct
import time

# Create a shorthand for gl
import bge
gl = bge.logic

# Globals for networking
user = 'Kupoman'
port = 9999
ip = 'localhost'
addr = (ip, port)

# Error handling global
gl.error = False

# Server script/runtime (in order of precedence)
servers = [
	"python server.py",
	"python server.pyc",
	"server.exe"
]
	
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
		if 'client' in main:
			main['client'].send("dis:"+main['client'].id)
			
		if hasattr(gl, "server"):
			gl.server.terminate()
			del gl.server
	except Exception as e:
		print(e)
	
	gl.error = True
	gl.endGame()
					
def in_game(cont):
	# Wrap this whole thing in a try/except to prevent console spam
	try:
		if gl.error:
			return
	
		own = cont.owner
		
		# Check for and handle exits
		if cont.sensors['exit'].positive:
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
		own['effect_system'] = EffectSystem(own['engine'])
		
	# Create a socket and register with the server
	if 'client' not in own:
		own['client'] = GameClient(user, addr)
		
		return
	elif not own['client'].connected:
		own['client'].run()
		if own['client'].server_addr == "0.0.0.0":
			# We failed to reach the server
			print("Failed to reach the server...")
			print("Starting local server")
			own['client'].restart(user, ('localhost', port))
			if hasattr(gl, 'server'):
				gl.server.terminate()
				
			# Find something to run
			server = ""
			for s in servers:
				if os.path.exists(s.split()[-1]):
					server = s
					break

			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			si.wShowWindow = 7 #SW_SHOWMINNOACTIVE
			gl.server = subprocess.Popen(s, startupinfo=si, creationflags=subprocess.CREATE_NEW_CONSOLE)
		
		return		
	
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
	
	# Setup the passive combat system
	own['state_manager'] = GameStateManager("CharacterCreation", own)
	own['init'] = True
	
