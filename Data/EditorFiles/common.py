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

import subprocess
import os

SETTINGS = {
	'blender_path': "",
	'text_editor_path': "",
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

def edit_text_file(file):
	editor = SETTINGS['text_editor_path']
	
	if not editor:
		print("WARNING: No text editor set")
		return
	
	p = subprocess.Popen([editor, file])
	