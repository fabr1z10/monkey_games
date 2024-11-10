import monkey
from . import values
from . import settings

class BubbleController(monkey.components.Controller2D):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.addCallback(self.minchia)

  def minchia(self, dt):

    self.node.move((dt,0))


class Bubble(monkey.Node):

	def minchia(self, dt):
		self.move((20*dt, 0, 0))
		if self.x > self.x0 + 64:
			ix = int(self.x//16)
			iy = int(self.y//16)
			self.direction = settings.bubinfo[iy][ix]
			print('going to ',self.direction)
			self.controller.setState(1)

	def minchia2(self, dt):
		if self.direction == 0:
			# find cell
			self.move((0,10*dt,0))
			iy = int((self.y - 8) // 16)
			ix = int(self.x // 16)
		elif self.direction == 1:
			self.move((0, -10 * dt, 0))
			iy = int((self.y + 8) // 16)
			ix = int(self.x // 16)
		elif self.direction == 2:
			self.move((-10 * dt, 0, 0))
			iy = int(self.y // 16)
			ix = int((self.x + 8) // 16)
		else:
			self.move((10 * dt, 0, 0))
			iy = int(self.y // 16)
			ix = int((self.x + 8) // 16)

		self.direction = settings.bubinfo[iy][ix]

	def __init__(self, x, y):
		super().__init__()
		self.direction = 0	# 0 = UP, 1 = DOWN, 2= LEFT,3 = RIGHT
		self.x0 = x
		self.set_position(x, y, 1)
		self.set_model(monkey.models.getSprite('gfx/bubble'), batch='gfx')
		self.collider = monkey.components.Collider(values.FLAG_BUBBLE, values.FLAG_PLAYER | values.FLAG_FOE,
			values.TAG_FOE, monkey.shapes.AABB(-8, 8, -8, 8))
		self.controller = monkey.components.Controller2D(size=(16, 16), speed=20, acceleration=500,
										 jump_height=0, time_to_jump_apex=0)
		self.controller.addCallback(self.minchia)
		self.controller.addCallback(self.minchia2)
		self.add_component(self.collider)
		self.add_component(self.controller)




class LinePlatform(monkey.Node):
	def __init__(self, x, y, width, oy=0):
		super().__init__()
		self.set_position(x, y)
		platform_width = width * values.TILESIZE
		self.add_component(monkey.components.Collider(values.FLAG_PLATFORM_SEMI, 0, 1,
			monkey.shapes.Segment(0, oy, platform_width, oy)))


class RectangularPlatform(monkey.Node):
	def __init__(self, x, y, tx, ty, width, height, tw=1, th=1):
		super().__init__()
		self.set_position(x, y)
		platform_width = width * tw * values.TILESIZE
		platform_height = height * th * values.TILESIZE
		tp= monkey.TileParser('gfx')
		self.set_model(tp.parse('Q {0},{1},{2},{3},{4},{5}'.format(tx, ty, tw, th, width, height)))
		self.add_component(monkey.components.Collider(values.FLAG_PLATFORM, 0, 1,
			monkey.shapes.AABB(0, platform_width, 0, platform_height)))




