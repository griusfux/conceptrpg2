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

#Import all effects into this file for one stop access
from Scripts.effects import *

		
class EffectManager:
	def __init__(self, engine):
		self._engine = engine
		self._local_effects = {}
		self._remote_effects = {}
		self._next_id = 0
		
	def add(self, effect, id=None, d=None):		
		if id == None:
			id = self._next_id
			
		if d is None:
			d = self._local_effects
			
		if id in d:
			if d == self._local_effects:
				print("WARNING: Local effect id already in use: %d. Skipping" % id)
			else:
				print("WARNING: Remote effect id already in use: %d. Skipping" % id)
			return -1
			
		d[id] = effect
		effect._load(id, self._engine)
		self._next_id += 1
		return effect.id
	
	def remove(self, id, d=None):
		# -1 indicates that the effect was never added
		if id == -1: return
		
		if d is None:
			d = self._local_effects
		
		effect = d.get(id)
		
		if not effect:
			if d == self._local_effects:
				print("WARNING: Could not find local effect id:", id)
			# XXX Do we want to print warnings for remotes too?
			return
		
		effect._unload(self._engine)
		del d[id]
		
	def add_remote(self, effect, id):
		if id is None: return
		
		self.add(effect, id, self._remote_effects)

	def remove_remote(self, id):
		self.remove(id, self._remote_effects)
		
	def update_remote_id(self, local_id, remote_id):
		if local_id not in self._local_effects:
			print("WARNING: Could not find local effect id for updating remote id:", local_id)
			return
		self._local_effects[local_id].remote_id = remote_id
		
	def get_remote_id(self, id):
		return self._local_effects[id].remote_id
		
	def update(self):		
		for d in (self._local_effects, self._remote_effects):
			for effect in [i for i in d.values()]:
				if effect.time <= 0:
					if not effect._fire(self._engine):
						self.remove(effect.id, d)
				else:
					effect._update(self._engine)
					effect.time -= 1