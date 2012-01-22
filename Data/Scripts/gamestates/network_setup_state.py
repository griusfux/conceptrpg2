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
	
	ui_layout = None
	
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