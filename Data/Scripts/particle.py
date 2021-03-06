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

import bge
import mathutils
import math
import random
from collections import OrderedDict

X_AXIS = mathutils.Vector((1, 0, 0))
Y_AXIS = mathutils.Vector((0, 1, 0))
Z_AXIS = mathutils.Vector((0, 0, 1))

class ParticleSystem():
	"""Simple particles System"""
	
	args = OrderedDict([
		("Particle Name", ""),
		("Particles Per Frame", 1),
		("X Angle", 30.0),
		("Y Angle", 30.0),
		("X Size", 0.0),
		("Y Size", 0.0),
		("Starting Velocity", 500.0),
		("Velocity Variance", 0.0),
		("Particle Life", 30),
		("Life Variance", 0.0),
		("Gravity", -9.8),
		])
		
	def __init__(self, base):
		self.object = base
	def start(self, args):
		self.valid = True
		self.particle = args['Particle Name']
		self.part_life = args['Particle Life']
		self.ppf_inv = 1/(args['Particles Per Frame'] if args['Particles Per Frame'] else 1)
		
		# Save directional variance as radians
		self.x_var = math.radians(args['X Angle'])
		self.y_var = math.radians(args['Y Angle'])
		
		# Save the offests
		self.x_off = args['X Size']
		self.y_off = args['Y Size']
		
		# Save variances
		self.velocity_var = args['Velocity Variance']
		self.life_variance = args['Life Variance']
		
		# Store a time step
		self.dt = 1/bge.logic.getLogicTicRate()
		
		# Precalculate gravity*dt^2
		self.gravity_dt = args['Gravity']*self.dt*self.dt
		
		# Precalculate velocity*dt
		self.start_velocity_dt = args['Starting Velocity'] * self.dt
		
		# Add the first particle into the list
		self.particle_list = [self.create_particle()]
		
	def update(self):
		frame_position = self.ppf_inv
		while frame_position <= 1:
			self.particle_list.append(self.create_particle(frame_position))
			frame_position += self.ppf_inv
			
		[self.update_particle(particle) for particle in self.particle_list]
	def create_particle(self, frame_position=0):
		# Add the particle
		scene = bge.logic.getCurrentScene()
		particle = scene.addObject(self.particle, self.object, 0)
		
		# Determine particle heading
		x_tilt = random.uniform(-self.x_var, self.x_var)
		y_tilt = random.uniform(-self.y_var, self.y_var)
		
		# Apply x offset
		x_dir = self.object.getAxisVect(X_AXIS)
		particle.worldPosition = particle.worldPosition.copy() + x_dir * random.uniform(-self.x_off, self.x_off)
		
		# Apply y offset
		y_dir = self.object.getAxisVect(Y_AXIS)
		particle.worldPosition = particle.worldPosition.copy() + y_dir * random.uniform(-self.y_off, self.y_off)
		
		# Determine the particle velocity vector
		velocity = self.object.getAxisVect(Z_AXIS)
		velocity.rotate(mathutils.Euler((x_tilt, 0, y_tilt)))
		
		# Assign the particle properties
		particle['life'] = self.part_life
		if self.life_variance > .0001:
			particle['life'] *= 1+random.uniform(-self.life_variance, self.life_variance)
		particle['velocity'] = velocity * self.start_velocity_dt
		if self.velocity_var > .0001:
			particle['velocity'] *= (1+random.uniform(-self.velocity_var, self.velocity_var))
		# Deal with subframe positioning
		if frame_position < 1:
			particle.worldPosition = particle.worldPosition + particle['velocity']*self.dt*frame_position
			
		particle['velocity'] *= self.dt
		
		# Return the particle
		return particle
		
	def update_particle(self, particle):
		# Update particle life
		if particle['life'] <= 0:
			self.particle_list.remove(particle)
			particle.endObject()
			return
		else:
			particle['life'] -= 1
			
		# Apply gravity to the particle's velocity
		particle['velocity'][2] += self.gravity_dt
		
		# Update particle position
		particle.worldPosition = particle.worldPosition + particle['velocity']
		
