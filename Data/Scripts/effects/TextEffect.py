from Scripts.effects import StaticEffect

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
		StaticEffect.__init__(self, None, position, duration, delay, continuous)
		self.fontid = 0
		self.pt_size = 20
		self.color = (1, 1, 1, 1)
		self.text = str(text)
		self.speed = 0 if static else .01
		
		self.position = list(self.position)
		
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

		# Setup the matrices
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glPushMatrix()
		bgl.glLoadIdentity()
		bgl.gluOrtho2D(0, view[2], 0, view[3])
		bgl.glMatrixMode(bgl.GL_MODELVIEW)
		bgl.glPushMatrix()
		bgl.glLoadIdentity()

		# Calculate x and y
		screen_coord = cam.getScreenPosition(self.position)
		x = screen_coord[0] * ras.getWindowWidth()
		y = ras.getWindowHeight() - (screen_coord[1] * ras.getWindowHeight())

		# Center the x
		text_width, text_height = blf.dimensions(self.fontid, self.text)
		x -= text_width / 2

		distance = cam.getDistanceTo(self.position)
		# Calculate scale
		if 1000 - distance > 0:
			scale = (1000 - distance) / 1000
		else:
			scale = 0
			
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
			if self.continuous > 0:
				self.time = self.continuous
				self.fired = False
				return True
			return False
			
		bge.logic.getCurrentScene().post_draw.append(self.draw)
		
		self.time = self.duration
		self.fired = True
		return True
		