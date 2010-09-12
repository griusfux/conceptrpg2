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

from Scripts.race_data import *
from Scripts.monster_data import *

from Scripts.blender_input_system import BlenderInputSystem

from Scripts.networking.game_client import GameClient

import subprocess
import pickle

# Create a shorthand for gl
import GameLogic as gl

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

def exit_game():
	print("Exiting...")
	try:
		if hasattr(gl, "server"):
			gl.server.terminate()
	except:
		pass
	gl.endGame()
					
def in_game(cont):
	# Wrap this whole thing in a try/except to prevent console spam
	try:
		if gl.error:
			return
	
		own = cont.owner
		
		# Check for and handle exits
		if cont.sensors['exit'].positive:
			exit_game()
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
				
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			si.wShowWindow = 7 #SW_SHOWMINNOACTIVE
			gl.server = subprocess.Popen("python server.py", startupinfo=si, creationflags=subprocess.CREATE_NEW_CONSOLE)
		
		return		
	
	# Setup an input system
	own['input_system'] = BlenderInputSystem('keys.conf', 'mouse.conf')
	
	# Add the player
	scene = gl.getCurrentScene()
	gameobj = scene.addObject("CharacterEmpty", own)
	
	# Now add the mesh and armature based on race data
	race = Race("DarkKnight")
	own['engine'].load_library(race)
	
	root_ob = scene.addObject(race.root_object, own)
	root_ob.setParent(gameobj)
	
	# Store the player
	player = PlayerLogic(BlenderWrapper.Object(gameobj, root_ob))
	
	# Load stats for the player
	player.load_stats(open('Kupoman.save', 'rb'))
	
	# Fill the player's hit points
	player.hp = player.max_hp
	
	# Give the player an attack power
	player.active_power = Power('Attack')
	
	own['net_players'] = {own['client'].id: player}
	own['player'] = player
	
	# Parent the camera to the player
	cam = scene.objects["Camera"]
	cam.setParent(scene.objects["TopDownEmpty"])
	cam_empty = scene.objects['CamEmpty']
	
	# Switch to the 3rd person camera
	cam3p = None
	for child in gameobj.childrenRecursive:
		if child.name == '3PCam':
			cam3p = child
			break
			
	if cam3p:
		own['3p_cam'] = BlenderWrapper.Camera(cam3p, cam_empty)
		own['top_down_camera'] = BlenderWrapper.Camera(scene.active_camera)
		scene.active_camera = own['3p_cam'].camera
		
	# Setup the passive combat system
	own['state_manager'] = GameStateManager("DungeonGeneration", own)
	own['init'] = True
	