# $Id$

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.blender_wrapper as BlenderWrapper
from Scripts.ui.blender_ui_system import *
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

# Create a shorthand for gl
import bge
gl = bge.logic

# Globals for networking
user = 'Kupoman'
port = 9999
ip = 'localhost'
addr = (ip, port)

# Camera globals
scale_max = 2
scale_min = 0.25

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
		
def camera(cont):
	cam = cont.owner
	scaler = cont.sensors['scale'].owner
	ray = cont.sensors['ray']
	cempty = cont.sensors['CamEmpty'].owner
	
	if not ray.hitObject:
		scale = scale_max
	else:
		scale = scaler.getDistanceTo(ray.hitPosition)

		if scale > scale_max:
			scale = scale_max
		elif scale < scale_min:
			scale = scale_min
			
	scaler.scaling = [scale, scale, scale]

	cont.activate(cont.actuators['ray_track'])
	cont.activate(cont.actuators['cam_track'])
	
	# Handle mouselook
	mouse = gl.mouse
	
	# Calculate the change in x
	dx = 0.5 - mouse.position[0]
	
	# Rotate the camera
	cempty.applyRotation((0, 0, dx*5))
	
	# Calculate the change in y
	dy = 0.5 - mouse.position[1]
	
	is_upright = cempty.localOrientation[2][2] >= 0.0
	is_facing_up = cempty.localOrientation[2][1] >= 0.0
	apply_rot = False
	
	# if not (bool(is_upright) ^ bool(not(bool(dy >= 0) ^ bool(is_facing_up)))):
		# apply_rot = True
	# if is_upright:
		# apply_rot = True
	# elif dy >= 0.0 and is_facing_up:
		# apply_rot = True
	# elif dy < 0.0 and not is_facing_up:
		# apply_rot = True
		
	# if apply_rot:
		# cempty.applyRotation((-dy*5, 0, 0))
	
	# if cempty.localOrientation[2][1] >= 0.0:
		# if dy > 0:
			# cempty.applyRotation((-dy*5, 0, 0))
	#else
	# Rotate the camera
	# cempty.applyRotation((-dy*5, 0, 0))
	
	# Reset the mouse
	mouse.position = (0.5, 0.5)

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
		
	# Create a socket and register with the server
	if 'client' not in own:
		own['client'] = GameClient(user, addr)
		
		# Fallback to offline mode
		# if not own['client'].connected:
			# print("Could not connect to the server, starting game in offline mode.")
			# own['is_offline'] = True
			# own['is_host'] = True
		# else:
			# own['is_host'] = own['client'].is_host
			# print("Username: %s\tIs host? %s" % (own['client'].user, 'True' if own['client'].is_host else 'False'))
			# own['is_offline'] = False
			# own['net_players'] = {}
		own['is_host'] = own['is_offline'] = True
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

		
	# Setup the passive combat system
	own['state_manager'] = GameStateManager("CharacterCreation", own)
	own['init'] = True
	