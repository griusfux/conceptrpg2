# $Id$

from Scripts.packages import Power

class PowerManager:
	"""This class is used to manage a player's powers"""
	
	def __init__(self, powers):
		"""PowerManager constructor"""
		
		# If the first item is a string, assume the rest are and load the powers
		if type(powers[0]) == str:
			powers = [Power(string) for string in powers]
		
		self._powers = powers
		
		self._current_power = 0
		
	def add(self, power):
		"""Add a power to the manager
		
		power -- the power to add
		
		"""
		
		self._powers.append(power)
		
	def remove(self, power):
		"""Remove a power from the manager
		
		power -- the power to remove
		
		"""
		
		self._powers.remove(power)
		
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