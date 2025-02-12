import monkey2

from .colour import Colour

LEGO_HOME = '/home/fabrizio/Downloads/complete/ldraw/'
PATH = [LEGO_HOME, LEGO_HOME + 'p/', LEGO_HOME + 'parts/', LEGO_HOME + 'parts/s/', '/home/fabrizio/monkey_games/lego/assets/']
IDENTITY = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
colors = dict()

# open a file looking in search path
def openFile(f: str):
	ff = f.replace('\\', '/')
	for p in PATH:
		try:
			file = open(p + ff, 'r')
			return file
		except:
			pass
	print(f" -- Cannot find {ff}")
	exit(1)

def initialize():
	f = openFile('LDConfig.ldr')
	for l in f.readlines():
		if not l:
			continue  # skip empties
		values = l.split()

		if values and values[0] == '0':
			if values[1] == '!COLOUR':
				colour = Colour(values)
				colors[colour.code] = colour
