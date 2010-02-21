# $Id$

# Description: A program that runs the game server
# Contributers: Mitchell Stokes

from Scripts.GameServer import GameServer
import time

def main():
	server = GameServer(('localhost', 9999))
	
	server.serve_forever()
	
if __name__ == "__main__":
	main()