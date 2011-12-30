import Scripts.packages as packages
import Scripts.mathutils as mathutils
import Scripts.character_logic as character

class StaticEffect:
	def __init__(self, visual, position, orientation, duration=0, delay=0, continuous=-1):
		self.visual = visual
		
		self.position = mathutils.Vector((0, 0, 0))
		self.orientation = orientation
		self.target = position
		self.duration = duration
		self.delay = delay
		self.continuous = continuous
		self.obj = None
		self.fired = False
		if isinstance(self.target, character.CharacterLogic):
			self.position = self.target.position
		else:
			self.position = self.target
			
	@staticmethod
	def create_from_info(info, translate):
		visual = info['visual']
		ori = mathutils.Quaternion(info['orientation'])
		ori = ori.to_matrix()
		
		pos = info['target']
		if isinstance(pos, str):
			pos = translate[pos]
		else:
			pos = mathutils.Vector(pos)
		
		del info['type']
		del info['visual']
		del info['orientation']
		del info['target']	
		effect = StaticEffect(visual, pos, ori, **info)
		
		return effect
			
	def get_info(self):
		info = {
				'type' : "StaticEffect",
				'visual' : self.visual,
				'orientation' : None,
				'target' : None,
				'duration' : self.duration,
				'delay' : self.delay,
				'continuous' : self.continuous,
				}
		q = self.orientation.to_quaternion()
		info['orientation'] = (q.w, q.x, q.y, q.z)
		
		if isinstance(self.target, character.CharacterLogic):
			info['target'] = self.target.id
		else:
			info['target'] = self.target.to_tuple()
		
		return info
	
	def _load(self, id, engine):
		self.id = id
		self.time = self.delay
		
	def _unload(self, engine):
		engine.remove_object(self.obj)
		
	def _update(self, engine):
		if isinstance(self.target, character.CharacterLogic):
			self.position = self.target.object.position
		else:
			self.postion = self.target
		
	def _fire(self, engine):
		if self.fired:
			if self.continuous >= 0:
				self._unload(engine)
				self.time = self.continuous
				self.fired = False
				return True
			return False
		engine.load_library(packages.Effect(self.visual))
		self.obj = engine.add_object(self.visual, self.position, self.orientation, time=0)
		
		if isinstance(self.target, character.CharacterLogic):
			self.obj.set_parent(self.target.object)
		
		self.time = self.duration
		self.fired = True
		return True
			
	