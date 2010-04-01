class MapData():
	"""A class to hold map data"""
	
	def __init__(self, datafile):	
		self.tiles = {}
		
		self.tiles['Starts'] = []
		self.tiles['Rooms'] = []
		self.tiles['Corridors'] = []
		self.tiles['Ends'] = []
		self.tiles['Doors'] = []
		self.tiles['Stairs'] = []
		self.tiles['Traps'] = []
		
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "start_tile":
				self.tiles['Starts'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "room_tile":
				self.tiles['Rooms'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "corridor_tile":
				self.tiles['Corridors'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "end_tile":
				self.tiles['Ends'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "door_tile":
				self.tiles['Doors'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "stair_tile":
				self.tiles['Stairs'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "trap_tile":
				self.tiles['Traps'].append((element.get("blend_obj"), element.get("blend_scene")))
			elif element.tag == "encounter_deck":
				self.encounter_deck = element.text