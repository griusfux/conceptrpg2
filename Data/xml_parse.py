from Scripts.ArchiveFile import MapFile
from Scripts.DungeonGenerator import DungeonGenerator

af = MapFile('Maps/ShipRuins')
if not af.Init:
	print("\nCould not open the archive file, exiting...")
else:
	dgen = DungeonGenerator(af)
	dgen.GenerateFirst(None)
	dgen.GenerateNext()

af.close()
