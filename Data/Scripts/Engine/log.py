class Log:
	def __init__(self, stream, log):
		self.stream = stream
		self.log = log
		
	def write(self, msg):
		self.stream.write(msg)
		self.log.write(msg)
		
	def close(self):
		self.log.close()
		
	def flush(self):
		self.stream.flush()