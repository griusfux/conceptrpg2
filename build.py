import sys
import os
import shutil
import struct
import subprocess

sys.path.append(os.path.abspath("Data"))

from Scripts.packages import *

INSTALL_DIRS = [
	"Audio",
	"EditorFiles",
	"Schemas",
	"Scripts",
	"Shops/.config",
	"Textures",
	"../Saves",
]

PACKAGES = [
	ActionSet,
	Class,
	Effect,
	EncounterDeck,
	Item,
	Armor,
	Weapon,
	Map,
	Monster,
	Power,
	Feat,
	Race,
	Shop,
	Status
]

INSTALL_FILES = [
	"icon.png",
	"keys.conf",
	"main.py",
	"mouse.conf",
]

def ct_ignore(dir, contents):
	return [i for i in contents if i.startswith('.') or i.endswith('.pyc') or i == '__pycache__']
	
def clear_py(dir):
	for f in os.listdir(dir):
		if f.endswith('.py'):
			os.remove(os.path.join(dir, f))
		elif os.path.isdir(os.path.join(dir, f)):
			if f == '__pycache__':
				shutil.rmtree(os.path.join(dir, f))
			else:
				clear_py(os.path.join(dir, f))


def WriteRuntime(player_path, blend_path, output_path):

    # Check the paths
    if not os.path.isfile(player_path):
        print("The player could not be found! Runtime not saved.")
        return
    
    # Check if we're bundling a .app
    # if player_path.endswith('.app'):
        # WriteAppleRuntime(player_path, output_path)
        # return
    
    # Get the player's binary and the offset for the blend
    file = open(player_path, 'rb')
    player_d = file.read()
    offset = file.tell()
    file.close()    
    
    # Get the blend data
    file = open(blend_path, 'rb')
    blend_d = file.read()
    file.close()
    
    # Create a new file for the bundled runtime
    output = open(output_path, 'wb')
    
    # Write the player and blend data to the new runtime
    output.write(player_d)
    output.write(blend_d)
    
    # Store the offset (an int is 4 bytes, so we split it up into 4 bytes and save it)
    output.write(struct.pack('B', (offset>>24)&0xFF))
    output.write(struct.pack('B', (offset>>16)&0xFF))
    output.write(struct.pack('B', (offset>>8)&0xFF))
    output.write(struct.pack('B', (offset>>0)&0xFF))
    
    # Stuff for the runtime
    output.write(b'BRUNTIME')
    output.close()
    
    # Make the runtime executable on Linux
    if os.name == 'posix':
        os.chmod(output_path, 0o755)

			
if __name__ == '__main__':
	try:
		shutil.rmtree("build")
	except:
		pass
		
	os.mkdir("build")
	os.mkdir("build/Data")
	os.chdir("Data")
	
	# Freeze files
	subprocess.call("C:/Python32/Scripts/cxfreeze.bat py_editor.pyw -s --base-name=Win32GUI --target-dir ../build/tmp")
	subprocess.call("C:/Python32/Scripts/cxfreeze.bat server.py -s --target-dir ../build/tmp")

		
	# Copy packed packages
	for cls in PACKAGES:
		print("Packing %s packages..." % cls.__name__)
		if cls.__name__ == "Item":
			os.makedirs(os.path.join("..", "build", "Data", "Items"))
		
		os.makedirs(os.path.join("..", "build", "Data", cls._dir))
		
		for pgk in cls.get_package_list(show_traceback=True):
			pgk.pack(os.path.join("..", "build", "Data", pgk._path))
	
	os.chdir("..")
	
	
	shutil.copy2(os.path.join("build", "tmp", "py_editor.exe"),
				 os.path.join("build", "Data", "py_editor.exe"))
	shutil.copy2(os.path.join("build", "tmp", "server.exe"),
				 os.path.join("build", "Data", "server.exe"))
	shutil.rmtree(os.path.join("build", "tmp"))
	
	# Copy files
	for file in INSTALL_FILES:
		shutil.copy2("Data/"+file, "Build/Data/"+file)
	
	# Copy directories
	for dir in INSTALL_DIRS:
		shutil.copytree("Data/"+dir, "build/Data/"+dir, ignore=ct_ignore)
		
	os.chdir("build/Data")
	# Compile py files
	subprocess.call("python -m compileall -bq .")
	clear_py(".")
	os.chdir("../..")
	
	# Now copy extern (this avoid compiling the modules in extern, which is known to cause problems)
	shutil.copytree("Data/extern", "build/Data/extern", ignore=ct_ignore)
	
	# Create the runtime
	print("Creating runtime...", end=' ')
	subprocess.call("xcopy release\\win64\\*.* build\\Data /Y /E /Q")
	WriteRuntime("build/Data/blenderplayer.exe", "Data/data.blend", "build/Data/data.exe")
	os.remove("build/Data/blenderplayer.exe")
	print("Done")
	