# $Id$

# Description: Main game loops to be used in various parts of the game
# Contributers: Mitchell Stokes

# Define all of the needed game loops here

import Scripts.ArchiveFile as ArchiveFile
from Scripts.DungeonGenerator import DungeonGenerator
from Scripts.CharacterLogic import PlayerLogic

from Scripts.BlenderObjectWrapper import BlenderObjectWrapper
from Scripts.BlenderInputSystem import BlenderInputSystem

# Create a shorthand for gl
import GameLogic as gl


def MainMenu(cont):
	pass

def InGame(cont):
	own = cont.owner


	# Start by loading the dungeon
	if 'dgen' not in own:	
		# Display the splash
		gl.addScene('Overlay')
		
		own['mapfile'] = ArchiveFile.MapFile('Maps/ShipRuins')
		
		if not own['mapfile'].init:
			print("Could not open the archive!")
			own['mapfile'].Close()
			del own['mapfile']
			return
		
		own['dgen'] = DungeonGenerator(own['mapfile'])
		own['dgen'].GenerateFirst(cont.owner)
		
	# Keep creating the dungeon if there are more tiles
	if own['dgen'].HasNext():
		own['dgen'].GenerateNext()
		return
	elif 'mapfile' in own:
		own['mapfile'].Close()
		del own['mapfile']
		
		print("\nDungeon generation complete\n")
		gl.getSceneList()[1].end()
	
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
		
		