import bpy

with open('grabber.txt', 'w') as f:
	for i in bpy.data.objects:
		f.write(i.name+"\n")