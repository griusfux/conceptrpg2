from Scripts.ArchiveFile import MapFile
#from Scripts.DungeonGenerator import DungeonGenerator

af = MapFile('Maps/ShipRuins')
if not af.init:
	print("\nCould not open the archive file, exiting...")
else:
	print("Success!\n")
	# dgen = DungeonGenerator(af)
	# dgen.GenerateFirst(None)
	# dgen.GenerateNext()

af.Close()
