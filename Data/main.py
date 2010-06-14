# $Id: GameLoops.py 29 2010-02-21 01:54:51Z Moguri $

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.blender_wrapper as BlenderWrapper
from Scripts.ui.blender_ui_system import *
from Scripts.archive_file import *
from Scripts.dungeon_generator import DungeonGenerator, EncounterDeck
from Scripts.character_logic import PlayerLogic, ProxyLogic, MonsterLogic
from Scripts.combat_system import CombatSystem

from Scripts.race_data import *
from Scripts.monster_data import *

from Scripts.blender_input_system import BlenderInputSystem

from Scripts.Networking.GameClient import GameClient

import subprocess
import pickle

# Create a shorthand for gl
import GameLogic as gl

# Globals for networking
user = 'Kupoman'
addr = ('192.168.1.5', 9999)

# Camera globals
scale_max = 1
scale_min = 0.25
	
def animation(cont):
	mess = cont.sensors['mess']

	if mess.positive:
		cont.activate(mess.bodies[0])
		
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

	
					
def in_game(cont):
	own = cont.owner
		
	if 'init' not in own:
		init(own)	
	elif own['init']:
		old_ori = own['cam_empty'].worldOrientation.copy()
		own['cam_empty'].localOrientation.identity()
		own['player'].obj.gameobj.localOrientation = old_ori
		# Do combat -- don't go past combant if we are still in combat
		if handle_combat(own):
			return
		
		if not own['is_offline']:
			handle_network(own)

		# Do input
		handle_input(own)
		
		# Check to see if the player should be triggering combat
		# gameobj = own['player'].obj.gameobj
		# if gameobj.sensors['sensor'].hitObject:
			# gameobj.sendMessage("encounter", str(gameobj.sensors['sensor'].hitObject.getPhysicsId()))
			
	# Always update the ui
	own['ui_system'].run()
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
		if not own['client'].connected:
			print("Could not connect to the server, starting game in offline mode.")
			own['is_offline'] = True
			own['is_host'] = True
		else:
			own['is_host'] = own['client'].is_host
			print("Username: %s\tIs host? %s" % (own['client'].user, 'True' if own['client'].is_host else 'False'))
			own['is_offline'] = False
			own['net_players'] = {}
			
	# Try to load the mapfile
	if 'mapfile' not in own:
		own['mapfile'] = MapFile('ShipRuins')
		
		if not own['mapfile'].init:
			print('Could not open the map file!')
			own['mapfile'].close()
			del own['mapfile']
			own['init'] = False
			return
			
		# Otherwise, load the scenes so the dungeon generator can use them
		gl.LibLoad(own['mapfile'].blend, 'Scene')

	# Start by loading the dungeon
	if 'dgen' not in own:	
		# Display the splash
		# if len(gl.getSceneList()) == 1:
			# gl.addScene('Overlay')
		own['ui_system'].load_layout('dun_gen')
		
		own['dgen'] = DungeonGenerator(own['mapfile'])
		
		if own['is_host']:
			own['dgen'].generate_first(own)
			own['client'].send_message('reset_map')
		elif own['is_offline']:
			own['dgen'].generate_first(own)
		else:
			result = []
			own['client'].send_message('get_map')
			
			cmd, data = own['client'].receive_message()
			
			# Hopefully this doesn't lock things for too long
			while cmd != 'end_map':
				if cmd == 'map' and data:
					result.append(pickle.loads(bytes(data, 'utf8')))
				cmd, data = own['client'].receive_message()
			
			print("The map size received was " + str(len(result)))
			own['dgen'].generate_from_list(own, result)
			
		# Give the engine a chance to catch up
		return
		
	# Keep creating the dungeon if there are more tiles
	if own['is_host'] and own['dgen'].has_next():
		own['dgen'].generate_next()
		return
	# Only check the dungeon if we're the host
	elif own['is_host'] and not own['dgen'].check_dungeon():
		# The dungeon is unacceptable, delete it and try again
		del own['dgen']
		for obj in gl.getCurrentScene().objects:
			if obj.name not in ("DungeonEmpty", "Lamp.001", "Camera"):
				obj.endObject()
		return
	elif 'mapfile' in own:
		own['mapfile'].close()
		del own['mapfile']

		# gl.getSceneList()[1].end()
		own['ui_system'].load_layout(None)
		print("\nDungeon generation complete with %d rooms\n" % own['dgen'].room_count)
		
		# If we're the host, send the map data to the server
		if own['is_host'] and not own['is_offline']:
			print("The map size sent was " + str(len(own['dgen'].result)))
			for i in own['dgen'].result:
				own['client'].send_message('set_map', pickle.dumps(i, 0), timeout=1)
		
	
	# Setup an input system
	own['input_system'] = BlenderInputSystem('keys.conf', 'mouse.conf')
	#own['input_system'].mouse.show(True)
	
	# Add the HUD
	gl.addScene('HUD')
	
	# Add the player
	scene = gl.getCurrentScene()
	temp = own.position
	temp[2] += 1
	own.position = temp
	gameobj = scene.addObject("CharacterEmpty", own)
	
	# Now add the mesh and armature based on race data
	race = RaceFile("DarkKnight")
	race_data = RaceData(race)
	gl.LibLoad(race.blend, "Scene", "Scene")
	race.close()
	
	root_ob = scene.addObject(race_data.root_object, own)
	root_ob.setParent(gameobj)
	
	# Store the player
	own['player'] = PlayerLogic(BlenderWrapper.Object(gameobj, root_ob))
	
	# Parent the camera to the player
	cam = scene.objects["Camera"]
	cam.setParent(scene.objects["TopDownEmpty"])
	own['cam_empty'] = scene.objects["CamEmpty"]
	
	# Switch to the 3rd person camera
	cam3p = None
	for child in gameobj.childrenRecursive:
		if child.name == '3PCam':
			cam3p = child
			break
			
	if cam3p:
		own['3pcam'] = cam3p
		scene.active_camera = cam3p
		
	
	own['init'] = True
	
def handle_network(own):
	# Handle network data
	cmd, rdata = own['client'].receive_message()
	if rdata:
		data = rdata.split()
		
		if cmd == 'update_player':
			if data[0] != own['client'].user and data[0] not in own['net_players']:
				gameobj = gl.getCurrentScene().addObject("CharacterEmpty", own)				
				own['net_players'][data[0]] = ProxyLogic(BlenderWrapper.Object(gameobj))
			
			own['net_players'][data[0]].update((data[1], data[2], data[3]), (data[4], data[5], data[6]))
		elif cmd == 'disconnect':
			if data[0] in own['net_players']:
				own['net_players'][data[0]].Die()
				del own['net_players'][data[0]]
				
def handle_combat(own):	
	# Detect combat and init
	if own.sensors['encounter_mess'].positive:
	
		# Get the room the encounter is taking place in
		room = own['dgen'].rooms[own.sensors['encounter_mess'].bodies[0]]
		
		# Generate an enemy list using the encounter deck
		enemy_list = own['dgen'].encounter_deck.generate_encounter(5)
		
		# Replace all the elements in the element list with MonsterLogic objects
		for monster in enemy_list:
			
			# Load the gameobject for the monster into the scene if it isn't already there
			if monster not in gl.getCurrentScene().objects:
				monsterfile = MonsterFile(monster)
				gl.LibLoad(monsterfile.blend, 'Scene', 'Scene')
				monsterfile.close()
				
			monster_object = None #BlenderWrapper.Object(gl.getCurrentScene().addObject(monster, own))
			monster_data = MonsterData(MonsterFile(monster))
			enemy_list[enemy_list.index(monster)] = MonsterLogic(monster_object, monster_data)

		own['combat_system'] = CombatSystem(own, BlenderWrapper.Object(own), own['engine'], enemy_list, BlenderWrapper.Object(room))
		
		# The combat system is setup, we don't need this anymore
		del room['encounter']
		
	# When the Combat System's update() returns false, combat is over
	if 'combat_system' in own:
		scene = gl.getCurrentScene()
		# scene.active_camera = scene.objects['Camera']
		if own['combat_system'].update(own):
			return True
		else:
			# Clean up
			print("Combat has finished")
			del own['combat_system']
			
	return False

def handle_input(own):	
	# Collect input
	inputs = own['input_system'].run()
	
	scene = gl.getCurrentScene()
	scene.active_camera = own['3pcam']
	
	# Check the input
	if inputs:
		if "SwitchCamera" in inputs:
			scene.active_camera = scene.objects['Camera']
			
		if "MoveForward" in inputs:
			old_ori = own['cam_empty'].worldOrientation.copy()
			own['cam_empty'].localOrientation.identity()
			own['player'].obj.gameobj.localOrientation = old_ori
		
		# Move the character
		own['player'].move_player(inputs, own['input_system'].mouse, own['client'])

