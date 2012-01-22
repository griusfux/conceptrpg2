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

import time
from collections import OrderedDict

class Profiler:
	
	def __init__(self):
		self.times = OrderedDict()
		
	def dump(self, log_name='profile_log.txt'):
		with open(log_name, 'a') as f:
			for name, times in self.times.items():
				avg_time = sum(times)/len(times)
				f.write("Average time for %s = %.4fus\n" % (name, avg_time*1000000))
		self.times = {}
		
	def start(self, name):
		t = time.clock()
		
		if name in self.times:
			self.times[name].append(t)
		else:
			self.times[name] = [t]
		
	def end(self, name):
		t = time.clock()
		time_spent = (t - self.times[name][-1])
		self.times[name][-1] = time_spent
#		avg_time = sum(self.times[name])/len(self.times[name])
#		print("Time for %s = %fus (avg: %fus)" % (name, time_spent, avg_time))
