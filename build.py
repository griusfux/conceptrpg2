import sys
sys.path.append("Data")


import os
import shutil
import struct
import subprocess
from Scripts.packages import *

INSTALL_DIRS = [
	"Actions/.config",
	"extern",
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
	"data.blend",
	"icon.png",
	"keys.conf",
	"main.py",
	"mouse.conf",
]

FREEZE_FILES = [
	"setup_editor.py",
	"setup_server.py"
]

# FREEZE_INSTALL = [
	# "server.exe",
	# "py_editor.exe",
	# "libgcc_s_dw2-1.dll",
	# "mingwm10.dll",
	# "PyQt4.QtCore.pyd",
	# "PyQt4.QtGui.pyd",
	# "python31.dll",
	# "QtCore4.dll",
	# "QtGui4.dll",
	# "sip.pyd"
# ]

def ct_ignore(dir, contents):
	return [i for i in contents if i.startswith('.') or i.endswith('.pyc')]
	
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
    output.write("BRUNTIME".encode())
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
	
	# Freeze files
	os.chdir("Data")
	# for ff in FREEZE_FILES:
		# subprocess.call("python "+ff+" build")
		
	# Copy packed packages
	for cls in PACKAGES:
		print("Packing %s packages..." % cls.__name__)
		if cls.__name__ == "Item":
			os.makedirs(os.path.join("..", "build", "Data", "Items"))
		
		os.makedirs(os.path.join("..", "build", "Data", cls._dir))
		
		for pgk in cls.get_package_list():
			pgk.pack(os.path.join("..", "build", "Data", pgk._path))
	
	os.chdir("..")
	# shutil.copytree("Data/build/exe.win32-3.1", "build/Data")
	# subprocess.call("xcopy Data\\build\\exe.win32-3.1\\*.* build\\Data /Y")
	# for fi in FREEZE_INSTALL:
		# shutil.copy2("Data/build/exe.win32-3.1/"+fi, "Build/Data/"+fi)
	
	# Copy files
	for file in INSTALL_FILES:
		shutil.copy2("Data/"+file, "Build/Data/"+file)
	
	# Copy directories
	for dir in INSTALL_DIRS:
		shutil.copytree("Data/"+dir, "build/Data/"+dir, ignore=ct_ignore)
		
	# Compile py files
	subprocess.call("python -m compileall -b build/Data")
	clear_py("build/Data")
	
	# Create the runtime
	print("Creating runtime...", end=' ')
	subprocess.call("xcopy release\\win64\\*.* build\\Data /Y /E")
	WriteRuntime("build/Data/blenderplayer.exe", "Data/data.blend", "build/Data/game.exe")
	# os.remove("build/Data/blenderplayer.exe")
	# os.remove("build/Data/data.blend")
	print("Done")
	