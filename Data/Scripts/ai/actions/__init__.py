import os, inspect

file = inspect.getfile(inspect.currentframe())
file = '/'.join(file.replace("\\", "/").split('/')[:-1])
for action in os.listdir(file):
	if action.startswith("."):
		continue
	if action.startswith("_"):
		continue
	if action == "__init__.py":
		continue
	
	action = action.split('.')[0]
	globals()[action] = __import__("Scripts.ai.actions."+action, fromlist=["Scripts.ai.actions"])