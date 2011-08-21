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
	
		p = subprocess.Popen([blender, '-b', "tmp", '-P', './EditorFiles/blender_grabber.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		p.wait()
		
		with open('grabber.txt') as f:
			retval = f.read().split()
		
	os.unlink('tmp')
	os.unlink('grabber.txt')
	
	return retval