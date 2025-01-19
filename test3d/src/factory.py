import monkey

LEGO_HOME = '/home/fabrizio/Downloads/complete/ldraw/'
PATH = [LEGO_HOME, LEGO_HOME + 'p/', LEGO_HOME + 'parts/']
#LEGO_MODEL = '35c01.dat'
LEGO_MODEL='48/1-4cyli.dat'
LEGO_MODEL='48/4-4cyli.dat'
colors = dict()

model_database = dict()

def openFile(f: str):
	ff = f.replace('\\', '/')
	for p in PATH:
		print('testing ',p+ff)
		try:
			file = open(p+ff, 'r')
			return file
		except:
			pass
	print('canmnot find ', ff)
	exit(1)
	return None

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


def LoadConfig():
    f = openFile('LDConfig.ldr')
    for l in f.readlines():
        if not l:
            continue  # skip empties
        values = l.split()

        if values and values[0] == '0':
            if values[1] == '!COLOUR':
                colour = Colour(values)
                colors[colour.code] = colour
    #for _, v in colors.items():
    #    print(v)

def move_cam(cam, by):
	def f():
		cam.move(by)
	return f

class LegoModel:
	def __init__(self, file: str, mainColor=None, transf=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]):
		self.submodels = []
		self.name = file
		self.transf = transf
		self.points = []
		self.colors = []
		f = openFile(file)
		if f:
			for line in f.readlines():
				if not line:
					continue
				values = line.split()
				if values:
					if values[0] == '1':
						# sub-file reference
						dep = values[-1]
						print('dependency', values)
						colour = int(values[1])
						assert(colour in colors)
						print(f"color={colors[colour].name}")
						fv = [float(x) for x in values[2:14]]
						sub_transf = [fv[3], fv[4], fv[5], 0,
						              fv[6], fv[7], fv[8], 0,
						              fv[9], fv[10], fv[11], 0,
						              fv[0], fv[1], fv[2], 1]
						self.submodels.append(LegoModel(dep, mainColor=colour, transf=sub_transf))
					elif values[0] == '4':
						# quadrilateral
						print(values)
						#print(colors)
						colour = int(values[1])
						print(colour)
						if colour == 16 and mainColor:
							colour = mainColor
						assert(colour in colors)
						col = colors[colour].value
						cc = monkey.from_hex(col[1:])
						print(f"color={colour} -> {colors[colour].name} ({col})")
						self.points.extend([float(values[2]), float(values[3]), float(values[4]),
							float(values[5]), float(values[6]), float(values[7]),
							float(values[8]), float(values[9]), float(values[10]),
							float(values[2]), float(values[3]), float(values[4]),
							float(values[11]), float(values[12]), float(values[13]),
							float(values[8]), float(values[9]), float(values[10])])
						self.colors.extend([cc[0], cc[1], cc[2], cc[3]])

	def instantiate(self):
		node = monkey.Node()
		model = monkey.models.TriangleModel('tri', color=self.colors, points=self.points)
		node.set_model(model)
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



def create_room():
	room = monkey.Room()
	cam = monkey.CamPerspective()
	room.add_camera(cam)
	room.add_batch('lines', monkey.LineBatch(max_elements=2000, cam=0))
	room.add_batch('tri', monkey.TriangleBatch(max_elements=10000, cam=0))
	monkey.engine().setCurrentRoom(room)
	cam.set_position([0, 0, 5], (0, 0, -1), (0, 1, 0))
	cam.set_position([0, 5, 0], (0, -1, 0), (0, 0, -1))

	LoadConfig()
	lm = LegoModel(LEGO_MODEL)
	#print(lm)
	n = monkey.Node()
	# open LDConfig.ldr


	#m = monkey.models.LineModel('lines', color=(1, 0, 0, 1), points=[0, 0, 0, 20, 0, 0])
	m = monkey.models.TriangleModel('tri', color =(1,0,0,1), points= [0,0,0,1,0,0,0.5,0.5,0])
	n.set_model(m)
	root = room.root()
	root.add(n)

	k = lm.instantiate()
	#k.setTransform([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0])
	root.add(k)

	kb = monkey.components.Keyboard()
	kb.add(265, 1, 0, move_cam(cam, (0, 0, -0.1)))
	kb.add(265, 2, 0, move_cam(cam, (0, 0, -0.1)))
	kb.add(264, 1, 0, move_cam(cam, (0, 0, 0.1)))
	kb.add(264, 2, 0, move_cam(cam, (0, 0, 0.1)))
	kb.add(262, 1, 0, move_cam(cam, (0.1, 0, 0)))
	kb.add(262, 2, 0, move_cam(cam, (0.1, 0, 0)))
	kb.add(263, 1, 0, move_cam(cam, (-0.1, 0, 0)))
	kb.add(263, 2, 0, move_cam(cam, (-0.1, 0, 0)))
	root.add_component(kb)

	return room
