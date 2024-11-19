import monkey

from . import settings

class RectangularPlatform(monkey.Node):
	def __init__(self, x, y, width, height, tw=1, th=1, tx=-1, ty=-1):
		super().__init__()
		print('called with',x,y,width,height,tw,th,tx,ty)
		self.set_position(x * settings.TILESIZE, y * settings.TILESIZE)
		platform_width = width * tw * settings.TILESIZE
		platform_height = height * th * settings.TILESIZE
		if tx != -1:
			tp= monkey.TileParser('gfx')
			self.set_model(tp.parse('Q {0},{1},{2},{3},{4},{5}'.format(tx, ty, tw, th, width, height)))
		if y < 24:
			self.add_component(monkey.components.Collider(settings.FLAG_PLATFORM_SEMI, 0, 1,
				monkey.shapes.AABB(0, platform_width, 0, platform_height)))

class Bubble(monkey.Node):
	def rm(node):
		node.remove()
	def __init__(self, x, y, flip):
		super().__init__()
		self.timer = 0
		self.timeout = 2225
		if x > 239.9 - 8:
			x = 239.9 - 8
		if x < 16.1 + 8:
			x = 16.1 + 8
		self.flip = flip
		self.direction = 0	# 0 = UP, 1 = DOWN, 2= LEFT,3 = RIGHT
		self.x0 = x - 16
		self.set_position(x, y, 1)
		bf = monkey.models.getSprite('gfx/bubble')
		bf.addFrameCallback('burst', 0, Bubble.rm)
		self.set_model(bf, batch='gfx')


		self.collider = monkey.components.Collider(settings.FLAG_BUBBLE, settings.FLAG_PLAYER | settings.FLAG_FOE,
			settings.TAG_BUBBLE, monkey.shapes.AABB(-8, 8, -8, 8))
		self.controller = monkey.components.Controller2D(size=(16, 16), speed=20, acceleration=500,
			jump_height=0, time_to_jump_apex=0)
		self.controller.addCallback(self.shoot)
		self.controller.addCallback(self.drift)
		self.controller.addCallback(self.burst)
		self.add_component(self.collider)
		self.add_component(self.controller)

	def shoot(self, dt):
		self.timer += dt
		f = -1 if self.flip else 1
		print(self.x)
		self.controller.move((f*settings.BUBBLE_SHOOT_SPEED*dt, 0), False)

		hit_wall = self.controller.left or self.controller.right
		x = self.x - 16
		y = self.y - 8
		if abs(x - self.x0) >= 64 or hit_wall:
			ix = int(x//8)
			iy = int(y//8)
			self.direction = settings.bubble_path[iy*28+ix]
			print('going to ',self.direction)
			self.controller.setState(1)

	def burst(self, dt):
		pass

	def blow_up(self):
		self.setAnimation('burst')
		self.controller.setState(2)

	def drift(self, dt):
		self.timer += dt
		if self.timer >= self.timeout:
			self.setAnimation('burst')
			self.controller.setState(2)
			return
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

		self.direction = settings.bubble_path[iy*28+ix]

