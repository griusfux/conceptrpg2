# $Id$

# Description: A program that runs the game server
# Contributers: Mitchell Stokes

import time
import sys

sys.path.append("extern")
from Scripts.networking.game_server import GameServer

class Log:
	def __init__(self, stream, log):
		self.stream = stream
		self.log = log
		
	def write(self, msg):
		self.stream.write(msg)
		self.log.write(msg)
		self.log.flush()
	
def main():
	log = open('server_log.txt', 'w')
	sys.stdout = Log(sys.stdout, log)
	server = GameServer(9999, 10)
	log.close()
	
if __name__ == "__main__":
	main()