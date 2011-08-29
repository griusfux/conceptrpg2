import subprocess
import os

SETTINGS = {
	'blender_path': ""
	}

def get_blender_objects(datafile):
	blender = SETTINGS['blender_path']
	
	if not blender:
		print("WARNING: BLENDER not set")
		return []
	
	
		
	with open("tmp", "wb") as f:
		f.write(datafile.blend)	
	
		p = subprocess.Popen([blender, '-b', "tmp", '-P', './extern/blender_grabber.py'],
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT,
								creationflags=subprocess._subprocess.SW_HIDE,)
		
		p.wait()
		
		with open('grabber.txt') as f:
			retval = f.read().split('\n')
		
	os.unlink('tmp')
	os.unlink('grabber.txt')
	
	return retval