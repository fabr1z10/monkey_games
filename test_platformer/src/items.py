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
		f = -1 if self.flip else 1
		self.move((f*settings.BUBBLE_SHOOT_SPEED*dt, 0, 0))
		x = self.x - 16
		y = self.y - 8
		if abs(x - self.x0) >= 64:
			ix = int(x//8)
			iy = int(y//8)
			self.direction = settings.bubinfo[iy*28+ix]
			print('going to ',self.direction)
			self.controller.setState(1)

	def minchia2(self, dt):
		x = self.x - 16
		y = self.y - 8
		if self.direction == 'U':
			# find cell
			self.move((0,settings.BUBBLE_DRIFT_SPEED*dt,0))
			iy = int((y - 4) // 8)
			ix = int(x // 8)
		elif self.direction == 'D':
			self.move((0, -settings.BUBBLE_DRIFT_SPEED * dt, 0))
			iy = int((y + 4) // 8)
			ix = int(x // 8)
		elif self.direction == 'L':
			self.move((-settings.BUBBLE_DRIFT_SPEED * dt, 0, 0))
			iy = int(y // 8)
			ix = int((x + 4) // 8)
		else:
			self.move((settings.BUBBLE_DRIFT_SPEED * dt, 0, 0))
			iy = int(y // 8)
			ix = int((x + 4) // 8)

		self.direction = settings.bubinfo[iy*28+ix]

	def __init__(self, x, y, flip):
		super().__init__()
		self.flip = flip
		self.direction = 0	# 0 = UP, 1 = DOWN, 2= LEFT,3 = RIGHT
		self.x0 = x - 16
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
	def __init__(self, x, y, width, height, tw=1, th=1, tx=-1, ty=-1):
		super().__init__()
		self.set_position(x, y)
		platform_width = width * tw * values.TILESIZE
		platform_height = height * th * values.TILESIZE
		if tx != -1:
			tp= monkey.TileParser('gfx')
			self.set_model(tp.parse('Q {0},{1},{2},{3},{4},{5}'.format(tx, ty, tw, th, width, height)))
		self.add_component(monkey.components.Collider(values.FLAG_PLATFORM_SEMI, 0, 1,
			monkey.shapes.AABB(0, platform_width, 0, platform_height)))




