# Define all of the needed game loops here

import Scripts.ArchiveFile as ArchiveFile
from Scripts.DungeonGenerator import DungeonGenerator

# Create a shorthand for gl
#import GameLogic as gl


def MainMenu(cont):
	pass

def InGame(cont):
	own = cont.owner

	# Start by loading the dungeon
	if 'dgen' not in own:
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
		
		