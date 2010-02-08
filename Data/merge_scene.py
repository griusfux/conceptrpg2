from Scripts.ArchiveFile import MapFile
from Scripts.DungeonGenerator import DungeonGenerator
import GameLogic as gl
def main(cont):
	own = cont.owner
	
	if 'dgen' not in own:
		own['map'] = MapFile('Maps/ShipRuins')
	
		if own['map'].init:
			own['dgen'] = DungeonGenerator(own['map'])
			
			own['dgen'].GenerateFirst(cont.owner)
		else:
			print("Unable to load mapfile: %s" % 'Maps/ShipRuins')
			own['map'].Close()
	else:
		if own['dgen'].HasNext():
			own['dgen'].GenerateNext()
		else:
			own['map'].Close()