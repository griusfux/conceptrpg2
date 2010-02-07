from ArchiveFile import MapFile
from DungeonGenerator import DungeonGenerator

af = MapFile('ShipRuins')
if not af.Init:
	print("\nCould not open the archive file, exiting...")
else:
	dgen = DungeonGenerator(af)
	dgen.GenerateFirst(None)
	dgen.GenerateNext()

af.close()
