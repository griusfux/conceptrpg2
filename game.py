import subprocess

subprocess.call("release/win64/blenderplayer.exe -w 1280 800 -m 4 -g show_framerate = 1 -g show_profile = 1 Data/data.blend",
				creationflags=subprocess.CREATE_NEW_CONSOLE)