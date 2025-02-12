import monkey2

from .util import *

class LegoModel:
	def __init__(self, file: str, mainColor=-1, transf=IDENTITY):
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
	def readSubFileReference(self, values: list):
		dep = values[-1]
		colour = int(values[1])
		if colour == 16:
			colour = self.mainColour
		fv = [float(x) for x in values[2:14]]
		sub_transf = [fv[3], fv[4], fv[5], 0,
			fv[6], fv[7], fv[8], 0,
			fv[9], fv[10], fv[11], 0,
			fv[0], -fv[1], -fv[2], 1]
		self.submodels.append(LegoModel(dep, mainColor=colour, transf=sub_transf))

	def readLine(self, values: list):
		cc = self.getColour(int(values[1]))
		fv = [float(x) for x in values[2:]]
		self.lines.extend( [fv[0], -fv[1], -fv[2], fv[3], -fv[4], -fv[5], cc[0], cc[1], cc[2], cc[3]] )
		#self.lineColors.extend([cc[0], cc[1], cc[2], cc[3]])

	def readTriangle(self, values: list):
		cc = self.getColour(int(values[1]))
		fv = [float(x) for x in values[2:]]
		#print(f"color={colour} -> {colors[colour].name} ({col})")
		self.points.extend([fv[0], -fv[1], -fv[2],
			fv[3], -fv[4], -fv[5],
			fv[6], -fv[7], -fv[8],
		    cc[0], cc[1], cc[2], cc[3]])

	def readQuad(self, values: list):
		cc = self.getColour(int(values[1]))
		fv = [float(x) for x in values[2:]]
		#print(f"color={colour} -> {colors[colour].name} ({col})")
		self.points.extend([fv[0], -fv[1], -fv[2],
			fv[3], -fv[4], -fv[5],
			fv[6], -fv[7], -fv[8],
			cc[0], cc[1], cc[2], cc[3],
			fv[0], -fv[1], -fv[2],
			fv[6], -fv[7], -fv[8],
			fv[9], -fv[10], -fv[11],
			cc[0], cc[1], cc[2], cc[3]])

	def getColour(self, id: int):
		if id == 16 and self.mainColour != -1:
			id = self.mainColour
			col = colors[id].value
		elif id == 24:
			id = self.mainColour if self.mainColour != -1 else id
			col = colors[id].edge
		else:
			col = colors[id].value
		return monkey2.fromHex(col)


	def instantiate(self):
		node = monkey2.Node()
		if self.points:
			#print('points:',self.points)
			model = monkey2.TriangleNormalModel(self.points)
			node.setModel(model,2)
		if self.lines:
			#print('lines:', self.lines)
			model = monkey2.LineModel(self.lines)
			lnode = monkey2.Node()
			lnode.setModel(model, 0)
			node.add(lnode)
		node.setTransform(self.transf)
		#print(f'instantiating {self.name} with transform {self.transf}')
		for s in self.submodels:
			node.add(s.instantiate())
		return node


	def __repr__(self, level=0):
		indent = "    " * level
		representation =  f"{indent}{self.name}\n"
		for sub in self.submodels:
			representation += sub.__repr__(level+1)
		return representation