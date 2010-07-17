# $Id$

# Description: A program that runs the game server
# Contributers: Mitchell Stokes

from Scripts.Networking.game_server import GameServer
import time

def main():
	server = GameServer(9999, 10)
	
if __name__ == "__main__":
	main()