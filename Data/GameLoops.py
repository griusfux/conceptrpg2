# $Id: GameLoops.py 29 2010-02-21 01:54:51Z Moguri $

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.ArchiveFile as ArchiveFile
from Scripts.DungeonGenerator import DungeonGenerator
from Scripts.CharacterLogic import PlayerLogic

from Scripts.BlenderObjectWrapper import BlenderObjectWrapper
from Scripts.BlenderInputSystem import BlenderInputSystem

import subprocess
import socket
import pickle
import codecs

# Create a shorthand for gl
import GameLogic as gl

# Globals for networking
is_host = True
user = b'Mog'
addr = ('localhost', 9999)
connected = False

def MainMenu(cont):
	pass
	
def Animation(cont):
	mess = cont.sensors['mess']
	
	if mess.positive:
		cont.activate(mess.bodies[0])

def InGame(cont):
	own = cont.owner

	# Start the server if we're the host
	#if is_host and "server_proc" not in own:
		#own['server_proc'] = subprocess.Popen("python server.py")
		
	# Create a socket and register with the server
	if 'socket' not in own:
		own['socket'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#own['socket'].setblocking(0)
		# Wait 10 seconds
		own['socket'].settimeout(10)

		own['socket'].sendto(b"register " + user, addr)
		print("Waiting on the server...")
		try:
			data = own['socket'].recv(1024)
			print("Reply received!")
			own['socket'].setblocking(0)
		except socket.timeout:
			print("Timed out while waiting on the server...")
		except socket.error:
			print("The server could not be reached...")
		

	# Start by loading the dungeon
	if 'dgen' not in own:	
		# Display the splash
		if len(gl.getSceneList()) == 1:
			gl.addScene('Overlay')
		
		own['mapfile'] = ArchiveFile.MapFile('Maps/ShipRuins')
		
		if not own['mapfile'].init:
			print("Could not open the archive!")
			own['mapfile'].Close()
			del own['mapfile']
			return
		
		own['dgen'] = DungeonGenerator(own['mapfile'])
		
		if is_host:
			own['dgen'].GenerateFirst(cont.owner)
		else:
			result = []
			own['socket'].sendto(b'get_map', addr)
			while True:
				try:
					data = own['socket'].recv(1024)
					result.append(pickle.loads(data))
					if not data:
						break
				except socket.error:
					break
			print("The map size is " + str(len(result)))
			own['dgen'].GenerateFromList(own, result)
			
		# Give the engine a chance to catch up
		return
		
	# Keep creating the dungeon if there are more tiles
	if own['dgen'].HasNext():
		own['dgen'].GenerateNext()
		return
	elif not own['dgen'].CheckDungeon():
		# The dungeon is unacceptable, delete it and try again
		del own['dgen']
		for obj in gl.getCurrentScene().objects:
			if obj.name not in ("DungeonEmpty", "Lamp.001", "Camera"):
				obj.endObject()
		return
	elif 'mapfile' in own:
		own['mapfile'].Close()
		del own['mapfile']

		gl.getSceneList()[1].end()
		print("\nDungeon generation complete with %d rooms\n" % own['dgen'].room_count)
		
		# If we're the host, send the map data to the server
		if is_host:
			print("The map size is " + str(len(own['dgen'].result)))
			for i in own['dgen'].result:
				msg = b'map ' + pickle.dumps(i, 0)
				own['socket'].sendto(msg, addr)
		
	
	# Setup an input system
	own['input_sys'] = BlenderInputSystem(cont.sensors['keyboard'], 'keys.conf')
	
	# Add the character
	scene = gl.getCurrentScene()
	if "CharacterEmpty" not in scene.objects:
		temp = own.position
		temp[2] += 1
		own.position = temp
		gameobj = scene.addObject("CharacterEmpty", own)
		
		own['character'] = PlayerLogic(BlenderObjectWrapper(gameobj))
	
	# Parent the camera to the player
	cam = scene.objects["Camera"]
	cam.setParent(own['character'].obj.gameobj)
	
	# Move the character
	inputs = own['input_sys'].Run()
	own['character'].PlayerPlzMoveNowzKThxBai(inputs)