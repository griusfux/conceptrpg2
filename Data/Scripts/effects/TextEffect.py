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

from Scripts.effects import StaticEffect
import Scripts.mathutils as mathutils

# Importing bge code, this prevents the server from chocking in it
try:
	import bgl
	import blf
	import bge
	import Rasterizer as ras
except:
	pass
	
class TextEffect(StaticEffect):
	def __init__(self, text, position, duration=30, delay=0, continuous=-1, static=False):
		ori  =[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
		StaticEffect.__init__(self, None, position, ori,
								duration, delay, continuous)
		self.fontid = 0
		self.pt_size = 20
		self.color = (1, 1, 1, 1)
		self.text = str(text)
		self.speed = 0 if static else .01
		
		self.static = static
		
		self.position = list(self.position)
	@staticmethod
	def create_from_info(info, translate):
		text = info['text']
		
		pos = info['target']
#		if isinstance(pos, str):
#			pos = translate[pos]
#		else:
#			pos = mathutils.Vector(pos)
		
		del info['type']
		del info['text']
		del info['target']	
		effect = TextEffect(text, pos, **info)
		
		return effect
			
	def get_info(self):
		info = {
				'type' : "TextEffect",
				'text' : self.text,
				'target' : self.position,
				'duration' : self.duration,
				'delay' : self.delay,
				'continuous' : self.continuous,
				'static' : self.static,
				}
		
#		if isinstance(self.target, character.CharacterLogic):
#			info['target'] = self.target.id
#		else:
#			info['target'] = self.target.to_tuple()
		
		return info
		
	def _unload(self, engine):
		bge.logic.getCurrentScene().post_draw.remove(self.draw)
		
	def draw(self):
		cam = bge.logic.getCurrentScene().active_camera
		
		self.position[2] += self.speed
		
		# Get some viewport info
		view_buf = bgl.Buffer(bgl.GL_INT, 4)
		bgl.glGetIntegerv(bgl.GL_VIEWPORT, view_buf)
		view = view_buf[:]

		if 0:
			# Save the state
			bgl.glPushAttrib(bgl.GL_ALL_ATTRIB_BITS)

			# Disable depth test so we always draw over things
			bgl.glDisable(bgl.GL_DEPTH_TEST)

			# Disable lighting so everything is shadless
			bgl.glDisable(bgl.GL_LIGHTING)

			# Unbinding the texture prevents BGUI frames from somehow picking up on
			# color of the last used texture
			bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)

			# Make sure we're using smooth shading instead of flat
			bgl.glShadeModel(bgl.GL_SMOOTH)


		# Calculate x and y
		screen_coord = cam.getScreenPosition(self.position)
		x = screen_coord[0] * ras.getWindowWidth()
		y = ras.getWindowHeight() - (screen_coord[1] * ras.getWindowHeight())
		
		# Check to make sure the position isn't behind the camera
		if not cam.pointInsideFrustum(self.position):
			return
	
		# Calculate scale
		distance = cam.getDistanceTo(self.position)
		if 1000 - distance > 0:
			scale = (1000 - distance) / 1000
		else:
			scale = 0

		# Setup the matrices
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glPushMatrix()
		bgl.glLoadIdentity()
		bgl.gluOrtho2D(0, view[2], 0, view[3])
		bgl.glMatrixMode(bgl.GL_MODELVIEW)
		bgl.glPushMatrix()
		bgl.glLoadIdentity()
		
		# Center the x
		text_width, text_height = blf.dimensions(self.fontid, self.text)
		x -= text_width / 2

			
		# Draw the font if large enough
		if scale:
			blf.size(self.fontid, int(self.pt_size*scale), 72)
			blf.position(self.fontid, x, y, 0)
			blf.draw(self.fontid, self.text)
			
		# Reset the state
		bgl.glPopMatrix()
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glPopMatrix()
		# bgl.glPopAttrib()
		
	def _fire(self, engine):
		if self.fired:
			if self.continuous >= 0:
				self._unload(engine)
				self.time = self.continuous
				self.fired = False
				return True
			return False

		bge.logic.getCurrentScene().post_draw.append(self.draw)
		
		self.time = self.duration
		self.fired = True
		return True
		