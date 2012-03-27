import subprocess
import os
import configparser
import sys
from collections import OrderedDict

CONFIG_NAME = "config.ini"
PLATFORMS = ('win64')

def main():
	config = configparser.ConfigParser()
	
	if CONFIG_NAME in os.listdir('.'):
		config.read(CONFIG_NAME)
	else:
		config['system'] =	OrderedDict([
								('debug', 'false'),
							])
		config['window'] =	OrderedDict([
								('fullscreen' , 'false'),
								('x_resolution' , '1280'),
								('y_resolution' , '800'),
								('aasamples' , '4'),
							])
		config['profile'] =	 OrderedDict([
								('show_fps' , 'false'),
								('show_profiler' , 'false'),
							])
		with open(CONFIG_NAME, 'w') as f:
			config.write(f)
	
	if len(sys.argv) > 1:
		platform = sys.argv[0]
		if platform not in PLATFORMS:
			print("%s is not a supported platform at this time" % platform)
			return
	else:
		platform = None
		
	args = []
	if platform:
		args.append("release/%s/blenderplayer.exe" % platform)
	else:
		args.append("Data/data.exe")
	args.append('-f' if config.getboolean('window', 'fullscreen') else '-w')
	args.append(config['window']['x_resolution'])
	args.append(config['window']['y_resolution'])
	args.append("-m %s" % config['window']['aasamples'])
	
	if config.getboolean('profile', 'show_fps'):
		args.append("-g show_framerate = 1")
	if config.getboolean('profile', 'show_profiler'):
		args.append("-g show_profile = 1")
	if config.getboolean('system', 'debug'):
		args.append("-c")
		
	if platform:
		args.append("Data/data.blend")
		subprocess.call(" ".join(args), creationflags=subprocess.CREATE_NEW_CONSOLE)
	else:
		subprocess.call(" ".join(args))
	
main()