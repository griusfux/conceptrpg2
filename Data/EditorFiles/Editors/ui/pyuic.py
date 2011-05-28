import subprocess
import sys

if __name__ == "__main__":
	file = sys.argv[1].split('\\')[-1]

	subprocess.call(r"python C:\Python32\Lib\site-packages\PyQt4\uic\pyuic.py -o "\
					+ file[:-3]+"_ui.py " +file)