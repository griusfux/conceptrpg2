# Description: A program that runs the game server
# Contributers: Mitchell Stokes

import time
import sys

sys.path.append("extern")
sys.path.append("2.61/python/lib") # Used in release configuration
from Scripts.networking.game_server import GameServer
from Scripts.Engine.log import Log

	
def main():
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 9999

	log = open('server_log.txt', 'w')
	sys.stdout = Log(sys.stdout, log)
	server = GameServer(port, 10)
	log.close()
	
if __name__ == "__main__":
	main()