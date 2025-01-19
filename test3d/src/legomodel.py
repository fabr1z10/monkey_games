import monkey

LEGO_HOME = '/home/fabrizio/Downloads/complete/ldraw/'
PATH = [LEGO_HOME, LEGO_HOME + 'p/', LEGO_HOME + 'parts/']
IDENTITY = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
colors = dict()


def openFile(f: str):
	ff = f.replace('\\', '/')
	for p in PATH:
		print('testing ', p + ff)
		try:
			file = open(p + ff, 'r')
			return file
		except:
			pass
	print('canmnot find ', ff)
	exit(1)
	return None

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

class Colour:
    def __init__(self, line):
        i = 3
        self.name = line[2]
        self.alpha = 255
        self.edge = None
        while i < len(line):
            if line[i] == 'CODE':
                self.code = int(line[i + 1])
                i += 2
            elif line[i] == 'VALUE':
                self.value = line[i + 1]
                i += 2
            elif line[i] == 'EDGE':
                self.edge = line[i + 1]
                i += 2
            elif line[i] == 'ALPHA':
                self.alpha = int(line[i + 1])
                i += 2
            else:
                i += 1

    def __repr__(self):
        return self.name + ' (' + str(self.code) + ') = ' + self.value + ', ' + str(self.alpha) + ', ' + str(self.edge)


class LegoModel:

	def readSubFileReference(self, values: list):
		dep = values[-1]
		colour = int(values[1])
		fv = [float(x) for x in values[2:14]]
		sub_transf = [fv[3], fv[4], fv[5], 0,
			fv[6], fv[7], fv[8], 0,
			fv[9], fv[10], fv[11], 0,
			fv[0], -fv[1], -fv[2], 1]
		self.submodels.append(LegoModel(dep, mainColor=colour, transf=sub_transf))

	def readLine(self, values: list):
		cc = self.getColour(int(values[1]))
		fv = [float(x) for x in values[2:]]
		self.lines.extend( [fv[0], -fv[1], -fv[2], fv[3], -fv[4], -fv[5]] )
		self.lineColors.extend([cc[0], cc[1], cc[2], cc[3]])

	def readTriangle(self, values: list):
		cc = self.getColour(int(values[1]))
		fv = [float(x) for x in values[2:]]
		#print(f"color={colour} -> {colors[colour].name} ({col})")
		self.points.extend([fv[0], -fv[1], -fv[2],
			fv[3], -fv[4], -fv[5],
			fv[6], -fv[7], -fv[8]])
		self.colors.extend([cc[0], cc[1], cc[2], cc[3]])

	def readQuad(self, values: list):
		cc = self.getColour(int(values[1]))
		fv = [float(x) for x in values[2:]]
		#print(f"color={colour} -> {colors[colour].name} ({col})")
		self.points.extend([fv[0], -fv[1], -fv[2],
			fv[3], -fv[4], -fv[5],
			fv[6], -fv[7], -fv[8],
			fv[0], -fv[1], -fv[2],
			fv[9], -fv[10], -fv[11],
			fv[6], -fv[7], -fv[8] ])
		self.colors.extend([cc[0], cc[1], cc[2], cc[3]])
		self.colors.extend([cc[0], cc[1], cc[2], cc[3]])

	def getColour(self, id: int):
		if id == 16 and self.mainColour:
			id = self.mainColour
			col = colors[id].value
		elif id == 24:
			id = self.mainColour if self.mainColour else id
			col = colors[id].edge
		else:
			col = colors[id].value
		return monkey.from_hex(col[1:])
	def __init__(self, file: str, mainColor=None, transf=IDENTITY):
		self.submodels = []
		self.mainColour = mainColor
		self.name = file
		self.transf = transf
		self.points = []
		self.colors = []
		self.lines = []
		self.lineColors = []
		f = openFile(file)
		if f:
			for line in f.readlines():
				if not line:
					continue
				values = line.split()
				if values:
					if values[0] == '1':
						self.readSubFileReference(values)
						# sub-file reference
					elif values[0] == '2':
						# line
						self.readLine(values)
					elif values[0] == '3':
						self.readTriangle(values)
					elif values[0] == '4':
						# quadrilateral
						self.readQuad(values)

	def instantiate(self):
		node = monkey.Node()
		if self.points:
			model = monkey.models.TriangleModel('tri', color=self.colors, points=self.points)
			node.set_model(model)
		if self.lines:
			model = monkey.models.LineModel('lines', color=self.lineColors, points = self.lines)
			lnode = monkey.Node()
			lnode.set_model(model)
			node.add(lnode)
		node.setTransform(self.transf)
		print('instantiating with transform',self.transf)
		for s in self.submodels:
			node.add(s.instantiate())
		return node


	def __repr__(self, level=0):
		indent = "    " * level
		representation =  f"{indent}{self.name}\n"
		for sub in self.submodels:
			representation += sub.__repr__(level+1)
		return representation