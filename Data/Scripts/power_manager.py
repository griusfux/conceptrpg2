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

# $Id$

from Scripts.packages import Power

class PowerManager:
	"""This class is used to manage a player's powers"""
	
	def __init__(self, owner, powers):
		"""PowerManager constructor"""
		self.owner = owner
		self._powers = []
		self._passives = []
		
		for power in powers:
			# If power is a string, load up the power package
			if type(power) == str:
				power = Power(power)
			# Filter the power into the appropriate list
			if "PASSIVE" in power.flags:
				self._passives.append(power)
			else:
				self._powers.append(power)
		
		self._current_power = 0
		
	def __iter__(self):
		return iter(self._powers)
		
	def add(self, power, controller):
		"""Add a power to the manager
		
		power -- the power to add
		
		"""
		
		if "PASSIVE" in power.flags:
			self._passives.append(power)
			power.push(controller, self.owner)
		else:
			self._powers.append(power)
		
	def remove(self, power, controller):
		"""Remove a power from the manager
		
		power -- the power to remove
		
		"""
		
		if "PASSIVE" in power.flags:
			self._passives.remove(power)
			power.pop(controller, self.owner)
		else:
			self._powers.remove(power)
			
	def __len__(self):
		return len(self._powers)
			
	def remove_all(self, controller):
		"""Remove all of the powers from the manager"""
		
		# Iterate a copy of the list so we aren't deleting
		# items through a list we're iterating.
		for i in self._powers[:]:
			self.remove(i, controller)
		
	def make_next_active(self):
		"""Make the power after the current power active"""
		
		if self._current_power == len(self._powers)-1:
			self._current_power = 0
		else:
			self._current_power += 1
			
	def make_prev_active(self):
		"""Make the power before the current power active"""
		
		if self._current_power == 0:
			self._current_power = len(self._powers) - 1
		else:
			self._current_power -= 1
			
	def has_power(self, idx):
		"""Checks to see if the supplied index is in the power list"""
		
		try:
			self._powers[idx]
			return True
		except IndexError:
			return False
			
	@property
	def all(self):
		"""All the powers returned as a list"""
		return self._powers
		
	@property
	def active_index(self):
		"""The index of the active power"""
		return self._current_power
		
	@property
	def active(self):
		"""The  currently active power"""
		
		return self._powers[self._current_power]
	
	def update_cooldown(self):
		for power in self.all:
			power.timer -= 1