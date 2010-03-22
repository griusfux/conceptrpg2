# $Id$

# Description: A program that runs the game server
# Contributers: Mitchell Stokes

from Scripts.Networking.GameServer import GameServer
import time

def main():
	server = GameServer(9999)
	
if __name__ == "__main__":
	main()