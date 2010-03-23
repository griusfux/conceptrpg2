# $Id: GameLoops.py 29 2010-02-21 01:54:51Z Moguri $

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.ArchiveFile as ArchiveFile
import Scripts.BlenderWrapper as BlenderWrapper
from Scripts.DungeonGenerator import DungeonGenerator, EncounterDeck
from Scripts.CharacterLogic import PlayerLogic, ProxyLogic
from Scripts.CombatSystem import CombatSystem

from Scripts.BlenderInputSystem import BlenderInputSystem

from Scripts.Networking.GameClient import GameClient

import subprocess
import pickle

# Create a shorthand for gl
import GameLogic as gl

# Globals for networking
user = 'Kupoman'
addr = ('192.168.1.5', 9999)

# Camera globals
scale_max = 4
scale_min = 1

def MainMenu(cont):
	pass
	
def Animation(cont):
	mess = cont.sensors['mess']
	
	if mess.positive:
		cont.activate(mess.bodies[0])
		
def Camera(cont):
	cam = cont.owner
	scaler = cont.sensors['scale'].owner
	ray = cont.sensors['ray']
	
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

	
					
def InGame(cont):
	own = cont.owner
		
	if 'init' not in own:
		Init(own)	
	elif own['init']:
		if not own['is_offline']:
			HandleNetwork(own)

		# Do combat
		HandleCombat(own)
		
		# Do input
		HandleInput(own)
		
		# Check to see if the player should be triggering combat
		# gameobj = own['character'].obj.gameobj
		# if gameobj.sensors['sensor'].hitObject:
			# gameobj.sendMessage("encounter", str(gameobj.sensors['sensor'].hitObject.getPhysicsId()))
			
def Init(own):
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
		own['mapfile'] = ArchiveFile.MapFile('ShipRuins')
		
		if not own['mapfile'].init:
			print('Could not open the map file!')
			own['mapfile'].close()
			del own['mapfile']
			own['init'] = False
			return

	# Start by loading the dungeon
	if 'dgen' not in own:	
		# Display the splash
		if len(gl.getSceneList()) == 1:
			gl.addScene('Overlay')
		
		own['dgen'] = DungeonGenerator(own['mapfile'])
		
		if own['is_host']:
			own['dgen'].GenerateFirst(own)
			own['client'].send_message('reset_map')
		elif own['is_offline']:
			own['dgen'].GenerateFirst(own)
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
			own['dgen'].GenerateFromList(own, result)
			
		# Give the engine a chance to catch up
		return
		
	# Keep creating the dungeon if there are more tiles
	if own['is_host'] and own['dgen'].HasNext():
		own['dgen'].GenerateNext()
		return
	# Only check the dungeon if we're the host
	elif own['is_host'] and not own['dgen'].CheckDungeon():
		# The dungeon is unacceptable, delete it and try again
		del own['dgen']
		for obj in gl.getCurrentScene().objects:
			if obj.name not in ("DungeonEmpty", "Lamp.001", "Camera"):
				obj.endObject()
		return
	elif 'mapfile' in own:
		own['mapfile'].close()
		del own['mapfile']

		gl.getSceneList()[1].end()
		print("\nDungeon generation complete with %d rooms\n" % own['dgen'].room_count)
		
		# If we're the host, send the map data to the server
		if own['is_host'] and not own['is_offline']:
			print("The map size sent was " + str(len(own['dgen'].result)))
			for i in own['dgen'].result:
				own['client'].send_message('set_map', pickle.dumps(i, 0), timeout=1)
		
	
	# Setup an input system
	own['input_sys'] = BlenderInputSystem(own.sensors['keyboard'], 'keys.conf')
	
	# Add the character
	scene = gl.getCurrentScene()
	temp = own.position
	temp[2] += 1
	own.position = temp
	gameobj = scene.addObject("CharacterEmpty", own)
	
	own['character'] = PlayerLogic(BlenderWrapper.Object(gameobj))
	
	# Parent the camera to the player
	cam = scene.objects["Camera"]
	cam.setParent(scene.objects["CamEmpty"])
	
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
	
def HandleNetwork(own):
	# Handle network data
	cmd, rdata = own['client'].receive_message()
	if rdata:
		data = rdata.split()
		
		if cmd == 'update_player':
			if data[0] != own['client'].user and data[0] not in own['net_players']:
				gameobj = gl.getCurrentScene().addObject("CharacterEmpty", own)				
				own['net_players'][data[0]] = ProxyLogic(BlenderWrapper.Object(gameobj))
			
			own['net_players'][data[0]].Update((data[1], data[2], data[3]), (data[4], data[5], data[6]))
		elif cmd == 'disconnect':
			if data[0] in own['net_players']:
				own['net_players'][data[0]].Die()
				del own['net_players'][data[0]]
				
def HandleCombat(own):
	#################
	## C O M B A T ##
	#################
	
	# Detect combat and init
	if own.sensors['encounter_mess'].positive:
	
		# Get the room the encounter is taking place in
		room = own['dgen'].rooms[own.sensors['encounter_mess'].bodies[0]]
		# Remove the encounter property from that room
		del room['encounter']
		# Generate an enemy list using the encounter deck, and initiate the combat system with it
		enemy_list = own['dgen'].encounter_deck.GenerateEncounter()
		own['combat_system'] = CombatSystem(BlenderWrapper.Object(own), BlenderWrapper.Engine, enemy_list, BlenderWrapper.Object(room))
		
		
	# When the Combat System's Update() returns false, combat is over
	if 'combat_system' in own:
		if own['combat_system'].Update() == False:
			# Clean up
			print("Combat has finished")
			del own['combat_system']

def HandleInput(own):	
	# Collect input
	inputs = own['input_sys'].Run()
	
	scene = gl.getCurrentScene()
	scene.active_camera = own['3pcam']
	
	# Check the input
	if inputs:
		if "SwitchCamera" in inputs:
			scene.active_camera = scene.objects['Camera']
		
		# Move the character
		own['character'].PlayerPlzMoveNowzKThxBai(inputs, own['client'])

