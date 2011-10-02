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
