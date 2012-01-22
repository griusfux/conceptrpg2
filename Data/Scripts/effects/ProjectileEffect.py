# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import Scripts.packages as packages
from Scripts.effects import StaticEffect
import Scripts.mathutils as mathutils

class ProjectileEffect(StaticEffect):
	def __init__(self, visual, position, target, speed=0.2, duration=10000, delay=0, continuous=-1):
		self.start = position
		if isinstance(target, mathutils.Vector):
			ori = target-position
		else:
			ori = target.object.position - position
			
		StaticEffect.__init__(self, visual, position, ori, duration, delay, continuous)
		
		self.target = target
		self.target_position = mathutils.Vector((0, 0, 0))
		self.speed = speed
		
		self.obj = None
		self.f_collision = None
			
	@staticmethod
	def create_from_info(info, translate):
		visual = info['visual']
		
		target = info['target']
		if isinstance(target, str):
			target = translate[target]
		else:
			target = mathutils.Vector(target)
		
		pos = mathutils.Vector(info['position'])
		
		del info['type']
		del info['visual']
		del info['target']
		del info['position']
		
		effect = ProjectileEffect(visual, pos, target, **info)
		
		return effect
			
	def get_info(self):
		info =StaticEffect.get_info(self)
		
		info['type'] = "ProjectileEffect"
		info['speed'] = self.speed
		info['position'] = self.start.to_tuple()
		
		del info['orientation']
		
		return info
		
	def _update(self, engine):
		if not self.obj:
			return
		
		if isinstance(self.target, mathutils.Vector):
			self.target_position = selft.target
		else:
			if not self.target.object.valid:
				self.time = 0
				return
			self.target_position = self.target.object.position
			
		self.target_position = self.target if isinstance(self.target, mathutils.Vector) else self.target.object.position
		self.target_position[2] += 1
		distance = self.target_position - self.obj.position
		
		if distance.length < 0.25:
			if self.f_collision:
				self.f_collision(self)
			self.time = 0
			
		else:
			velocity = distance.copy()
			velocity.normalize()
			
			up = mathutils.Vector((0,0,1))
			cross = velocity.cross(up)
			cross.normalize()
			up = velocity.cross(cross)
			up.normalize()
			
			matrix = mathutils.Matrix((cross, velocity, up))
			
			velocity *= self.speed
			self.obj.position += velocity
			
			orientation = matrix - self.obj.get_orientation().copy()
			orientation *= self.speed/2
			self.obj.set_orientation(self.obj.get_orientation()+orientation)
			# self.obj.set_orientation(matrix)#*(self.speed/2))
			
		
	def _fire(self, engine):
		return StaticEffect._fire(self, engine)
		
	def _unload(self, engine):
		StaticEffect._unload(self, engine)