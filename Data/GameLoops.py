# $Id: GameLoops.py 29 2010-02-21 01:54:51Z Moguri $

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.ArchiveFile as ArchiveFile
from Scripts.DungeonGenerator import DungeonGenerator
from Scripts.CharacterLogic import PlayerLogic

from Scripts.BlenderObjectWrapper import BlenderObjectWrapper
from Scripts.BlenderInputSystem import BlenderInputSystem

from Scripts.Networking.GameClient import GameClient

import subprocess
import pickle

# Create a shorthand for gl
import GameLogic as gl

# Globals for networking
is_host = True
user = 'Mog'
addr = ('localhost', 9999)

def MainMenu(cont):
	pass
	
def Animation(cont):
	mess = cont.sensors['mess']
	
	if mess.positive:
		cont.activate(mess.bodies[0])

def InGame(cont):
	own = cont.owner
	
		
	if 'init' not in own:
		# Create a socket and register with the server
		if 'client' not in own:
			own['is_host'] = is_host
			own['client'] = GameClient(user, addr)
			
			# Fallback to offline mode
			if not own['client'].connected:
				print("Could not connect to the server, starting game in offline mode.")
				own['is_offline'] = True
				own['is_host'] = True
			else:
				own['is_offline'] = False
				own['net_players'] = {}
				
		# Try to load the mapfile
		if 'mapfile' not in own:
			own['mapfile'] = ArchiveFile.MapFile('Maps/ShipRuins')
			
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
			
			if own['is_host'] or own['is_offline']:
				own['dgen'].GenerateFirst(cont.owner)
				own['client'].send_message('start_map')
			else:
				result = []
				own['client'].send_message('get_map')
				
				cmd, data = own['client'].receive_message()
				
				# Hopefully this doesn't lock things for too long
				while cmd != 'end_map':
					if cmd == 'map' and data:
						result.append(pickle.loads(bytes(data, 'utf8')))
					print((cmd, data))
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
					#msg = b'map ' + pickle.dumps(i, 0)
					#own['socket'].sendto(msg, addr)
					own['client'].send_message('send_map', pickle.dumps(i, 0))
			
		
		# Setup an input system
		own['input_sys'] = BlenderInputSystem(cont.sensors['keyboard'], 'keys.conf')
		
		# Add the character
		scene = gl.getCurrentScene()
		temp = own.position
		temp[2] += 1
		own.position = temp
		gameobj = scene.addObject("CharacterEmpty", own)
		
		own['character'] = PlayerLogic(BlenderObjectWrapper(gameobj))
		
		# Parent the camera to the player
		cam = scene.objects["Camera"]
		cam.setParent(own['character'].obj.gameobj)
		
		own['init'] = True
	# End init
	
	elif own['init']:
		if not own['is_offline']:
			cmd, rdata = own['client'].receive_message()
			if rdata:
				data = rdata.split()
				
				if cmd == 'update_player':
					if data[0] not in own['net_players']:
						gameobj = gl.getCurrentScene().addObject("CharacterEmpty", own)				
						own['net_players'][data[0]] = ProxyLogic(gameobj)
					
					own['net_players'][data[0]].Update(data[1], data[2])
		
		# Move the character
		inputs = own['input_sys'].Run()
		own['character'].PlayerPlzMoveNowzKThxBai(inputs, own['client'])