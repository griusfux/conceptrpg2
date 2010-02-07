#from ArchiveFile import MapFile
import GameLogic as gl
import lxml.etree
def main():
	#gl.LibLoad('Maps/ShipRuins/map.blend', "Scene")
	gl.LibLoad('Maps/MapOne/map.blend', "Scene", 'Scene')
	#print(gl.LibList())
	# map = MapFile('MapOne')

	# if af.Init:
		# gl.LibLoad(map.Blend, "Scene")
	# else:
		# print("Could not init")
		
	# map.close()