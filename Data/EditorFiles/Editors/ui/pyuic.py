import subprocess
import sys

if __name__ == "__main__":
	subprocess.call(r"python C:\Python31\Lib\site-packages\PyQt4\uic\pyuic.py -o "\
					+ sys.argv[1][:-3]+"_ui.py " +sys.argv[1])