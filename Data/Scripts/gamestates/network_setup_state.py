from .base_state import BaseState
import subprocess
import os

from Scripts.networking.game_client import GameClient

# Server script/runtime (in order of precedence)
servers = [
	"python ./server.py",
	"python ./server.pyc",
	"./server.exe"
]

class NetworkSetupState(BaseState):
	"""This states handles setting up the networking (start or join)"""
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		if main['is_host']:
			print("Starting local server")
			
			server = ""
			for s in servers:
				if os.path.exists(s.split()[-1]):
					server = s
					break
				
			server += " "+str(main['addr'][1])
			
			si = None
			if os.name == 'nt':
				si = subprocess.STARTUPINFO()
				si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
				si.wShowWindow = 7 #SW_SHOWMINNOACTIVE
			main['server'] = subprocess.Popen(s, startupinfo=si, creationflags=subprocess.CREATE_NEW_CONSOLE)
		
		
		main['client'] = GameClient(main['user'], main['addr'])
		
	def client_run(self, main):
		"""Client-side run method"""
		
		if main['client'].connected and main['client'].server_addr == "0.0.0.0":
			print("Failed to reach the server...")
			return ("Title", "SWITCH")
		
		if main['client'].registered:
			return ("CharacterSelect", "SWITCH")