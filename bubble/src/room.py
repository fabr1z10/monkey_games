import monkey
from . import settings
from .items import RectangularPlatform
from .bub import Bub
from re import sub

class GameRoom(monkey.Room):
	def __init__(self):
		super().__init__()
		self.height = 25                # height in tiles
		self.width = 28                 # width in tiles
		self.shade_tiles = {
			(0, 0, 1): (1, 2),
			(0, 1, 0): (2, 2),
			(0, 1, 1): (1, 1),
			(1, 0, 0): (2, 1),
			(1, 0, 1): (0, 1),
			(1, 1, 0): (0, 2),
			(1, 1, 1): (0, 1)
		}
		dw = settings.device_size[0]
		dh = settings.device_size[1]
		cam = monkey.CamOrtho(dw, dh,
							  viewport=(0, 0, dw, dh),
							  bounds_x=(dw//2, dw//2), bounds_y=(dh//2, dh//2))
		self.add_camera(cam)
		collision_engine = monkey.CollisionEngine2D(64, 64)
		#collision_engine.addResponse(MarioVsGoomba(values.TAG_PLAYER, values.TAG_FOE))
		self.add_runner(collision_engine)
		root = self.root()
		kb = monkey.components.Keyboard()
		kb.add(299, 1, 0, lambda: monkey.close_room())
		root.add_component(kb)
		self.add_batch('lines', monkey.LineBatch(max_elements=800, cam=0))
		self.add_batch('gfx', monkey.SpriteBatch(max_elements=10000, cam=0, sheet='bubble'))
		monkey.engine().setCurrentRoom(self)
		li = settings.level_data[settings.level]
		settings.bubble_path = GameRoom.rle_decode(li['bubble'])
		print(settings.bubble_path)
		#p =
		root.add(self.generatePlatforms(li))
		root.add(self.generateSide(0, 0, li))
		root.add(self.generateSide(30, 0, li))

		root.add(Bub(24, 8.1, 'gfx/bub', 6, 16, slide='walk', jumpUp='jump_up'))


	def rle_decode(s: str):
		return sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)), s)


	def generatePlatforms(self, desc):
		ix = 0
		iy = 0
		level = monkey.Node()
		level.set_position(16, 0)
		self.array = [[0 for _ in range(self.width)] for _ in range(self.height)]
		i = 0
		a = desc['desc']
		tile = desc['tile']
		while i < len(a):
			if a[i] == 0 or a[i] == 1:
				self.array[iy][ix] = a[i]
				ix += 1
				if ix >= self.width:
					ix = 0
					iy += 1
				i += 1
			else:
				for j in range(a[i]):
					self.array[iy][ix] = a[i + 1]
					ix += 1
					if ix >= self.width:
						ix = 0
						iy += 1
				i += 2
		# reset counters
		ix = 0
		iy = 0
		while iy < self.height:
			while ix < self.width:
				if self.array[iy][ix] == 1:
					# set initial platform dimensions
					w = 1
					h = 1
					extend = True
					while extend:
						# try extending horizontally
						ext_hor = ix + w < self.width
						if ext_hor:
							for u in range(h):
								if self.array[iy + u][ix + w] != 1:
									ext_hor = False
									break
							if ext_hor:
								w += 1
						ext_ver = iy + h < self.height
						if ext_ver:
							for u in range(w):
								if self.array[iy + h][ix + u] != 1:
									ext_ver = False
									break
							if ext_ver:
								h += 1
						extend = ext_hor or ext_ver
					print('found platorm at', ix, iy, 'size is', w, h)
					for u in range(ix, ix + w):
						for v in range(iy, iy + h):
							self.array[v][u] = 2
					p = RectangularPlatform(ix, iy, w, h, tw=1, th=1, tx=tile[0], ty=tile[1])
					level.add(p)
				ix += 1
			ix = 0
			iy += 1
		# change all 2s to 1s
		self.array = [[1 if i != 0 else 0 for i in row] for row in self.array]
		level.add(self.generateShade(desc))
		return level

	def generateSide(self, x, y, desc):
		side_desc = desc['side']
		tp = monkey.TileParser('gfx')
		s = monkey.Node()
		s.set_position(x * settings.TILESIZE, y * settings.TILESIZE)
		s.set_model(tp.parse(side_desc))
		s.add_component(monkey.components.Collider(settings.FLAG_PLATFORM, 0, 1,
			monkey.shapes.AABB(0, 16, 0, 25 * 8)))
		return s
		#root.add(leftSide)

	def generateShade(self, desc):
		pal = desc['pal']
		tp = monkey.TileParser('gfx')
		shade_str = 'PAL {0};'.format(pal)
		i = 0
		j = 0
		while i < self.height:
			while j < self.width:
				# in order to determine shader, for ij I need to check the 3 neighboring cells
				# i(j-1), (i+1)(j-1), i+1(j), which we call a, b and c
				if self.array[i][j] == 1:
					j += 1
					continue
				a = 1 if j == 0 else self.array[i][j - 1]
				b = 0 if i == self.height - 1 else 1 if j == 0 else self.array[i + 1][j - 1]
				c = 0 if i == self.height - 1 else self.array[i + 1][j]

				if a == 0 and b == 0 and c == 0:
					j += 1
					continue
				tile = self.shade_tiles[(a, b, c)]
				#print('add shade at', j, i)
				shade_str += 'GO {0},{1};Q {2},{3},1,1,1,1;'.format(j, i, tile[0], tile[1])
				j += 1
			i += 1
			j = 0
		shadeNode = monkey.Node()
		shade_str += 'PAL 0;'
		shadeNode.set_model(tp.parse(shade_str))
		return shadeNode
