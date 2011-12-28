import subprocess
import os
import configparser
from collections import OrderedDict

CONFIG_NAME = "config.ini"
PLATFORMS = ('win64')

def main():
	config = configparser.ConfigParser()
	
	if CONFIG_NAME in os.listdir('.'):
		config.read(CONFIG_NAME)
	else:
		config['system'] =	OrderedDict([
								('platform' , 'win64'),
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
		
	args = []
	
	platform = config['system']['platform']
	if platform not in PLATFORMS:
		print("%s is not a supported platform at this time" % platform)
		return
	
	args.append("release/%s/blenderplayer.exe" % platform)
	args.append('-f' if config.getboolean('window', 'fullscreen') else '-w')
	args.append(config['window']['x_resolution'])
	args.append(config['window']['y_resolution'])
	args.append("-m %s" % config['window']['aasamples'])
	
	if config.getboolean('profile', 'show_fps'):
		args.append("-g show_framerate = 1")
	if config.getboolean('profile', 'show_profiler'):
		args.append("-g show_profile = 1")
		
	args.append("Data/data.blend")
		
	subprocess.call(" ".join(args), creationflags=subprocess.CREATE_NEW_CONSOLE)
	
main()