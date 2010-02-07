#from ArchiveFile import MapFile
import GameLogic as gl
#import lxml.etree
def main():
	#gl.LibLoad('ShipRuins/map.blend', "Scene")
	gl.LibLoad('MapOne/map.blend', "Scene", 'Scene')
	gl.LibLoad('MapOne/map.blend', "Scene", 'Scenes')
	#print(gl.LibList())
	# map = MapFile('MapOne')

	# if af.Init:
		# gl.LibLoad(map.Blend, "Scene")
	# else:
		# print("Could not init")
		
	# map.close()