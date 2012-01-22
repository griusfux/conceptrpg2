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

class FadeEffect:
	def __init__(self, target, duration=60, amount=-1):
		self.target = target
		self.object = target.object
		self.time = duration
		self.amount = amount / duration
		
		self.remote_id = None
		self.f_end = None
			
	@staticmethod
	def create_from_info(info, translate):
		
		if info['target'] in translate:
			target = translate[info['target']]
		else:
			return None
		
		effect = FadeEffect(target, info['duration'], info['amount'])
		
		return effect
			
	def get_info(self):
		info = {
				'type' : "FadeEffect",
				'target' : self.target.id,
				'duration' : self.time,
				'amount' : self.amount * self.time,
				}
		
		return info
		
	def _load(self, id, engine):
		self.id = id
		
	def _unload(self, engine):
		if self.f_end:
			self.f_end(self.object, engine)
		
	def _update(self, engine):
		if self.object.valid:
			color = self.object.color
			color[3] += self.amount
			self.object.color = color

	def _fire(self, engine):
		pass
