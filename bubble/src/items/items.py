import monkey

from . import settings
from .foes import ZenChan, DeadFoe
from typing import Type, TypeVar, Generic


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
			self.add_component(monkey.components.Collider(settings.FLAG_PLATFORM_SEMI, 0, settings.TAG_PLATFORM,
				monkey.shapes.AABB(0, platform_width, 0, platform_height)))

class BubbleShoot(monkey.ControllerState):
	def start(self):
		self.timer = 0
		self.f = -1 if self.node.flip else 1
		self.x0 = self.node.x

	def update(self, dt):
		self.timer += dt

		self.node.controller.move((self.f * settings.BUBBLE_SHOOT_SPEED * dt, 0), False)
		hit_wall = self.node.controller.left or self.node.controller.right
		x = self.node.x - 16
		y = self.node.y - 8
		if abs(x - self.x0) >= 64 or hit_wall:
			ix = int(x//8)
			iy = int(y//8)
			self.direction = settings.bubble_path[iy*28+ix]
			self.node.controller.setState(1)

class BubbleDrift(monkey.ControllerState):
	def start(self):
		self.timer = 0
		self.timeout = 10
		self.timeout2 = 12
		self.frame = 0
		self.direction = 0	# 0 = UP, 1 = DOWN, 2= LEFT,3 = RIGHT


	def update(self, dt):
		self.timer += dt
		self.frame += 1
		if self.timer >= self.timeout:
			# blink before burst
			c = (self.frame // 6) % 2
			self.node.getRenderer().setState(monkey.NodeState.ACTIVE if c == 0 else monkey.NodeState.INACTIVE)
			#self.node.setAnimation('burst')
		if self.timer >= self.timeout2:
			self.node.burstAfterTimeout()
			return

		x = self.node.x - 16
		y = self.node.y - 8
		if self.direction == 'U':
			# find cell
			self.node.move((0, settings.BUBBLE_DRIFT_SPEED * dt,0))
			iy = int((y - 4) // 8)
			ix = int(x // 8)
		elif self.direction == 'D':
			self.node.move((0, -settings.BUBBLE_DRIFT_SPEED * dt, 0))
			iy = int((y + 4) // 8)
			ix = int(x // 8)
		elif self.direction == 'L':
			self.node.move((-settings.BUBBLE_DRIFT_SPEED * dt, 0, 0))
			iy = int(y // 8)
			ix = int((x + 4) // 8)
		else:
			self.node.move((settings.BUBBLE_DRIFT_SPEED * dt, 0, 0))
			iy = int(y // 8)
			ix = int((x + 4) // 8)
		self.direction = settings.bubble_path[iy*28+ix]

class BubbleBurst(monkey.ControllerState):
	def start(self):
		self.node.setAnimation('burst')





class BubbleToFoe(monkey.ControllerState):
	def start(self):
		# create foe
		z = ZenChan(self.node.x, self.node.y, -1, pal='angry_zenchan')
		self.node.parent.add(z)
		self.node.remove()



# we have different bubbles - bubbles fired by player,
# bubbles with flashes, water etc., foe bubbles,
# extend bubbles
class BubbleBase(monkey.Node):

	def common(self, x , y, model, mask):
		self.timer = 0
		# time after bubble bursts
		self.timeout = 10
		if x > 239.9 - 8:
			x = 239.9 - 8
		if x < 16.1 + 8:
			x = 16.1 + 8
		# store bubble initial position
		self.x0 = x - 16
		self.set_position(x, y, 1)
		bf = monkey.models.getSprite(model)
		# bf.addFrameCallback('burst', 0, Bubble.rm)
		self.set_model(bf, batch='gfx')

		self.collider = monkey.components.Collider(settings.FLAG_BUBBLE, mask,
		                                           settings.TAG_BUBBLE, monkey.shapes.AABB(-8, 8, -8, 8))

		self.controller = monkey.components.Controller2D(size=(16, 16),
		                                                 speed=20, acceleration=500, jump_height=0, time_to_jump_apex=0)
		self.add_component(self.collider)
		self.add_component(self.controller)

	def __init__(self, x, y, model, mask):
		super().__init__()
		self.common(x, y, model, mask)




	def burstAfterTimeout(self):
		pass

	def burstByPlayer(self):
		pass




class Bubble(BubbleBase):
	def rm(node):
		node.remove()

	def __init__(self, x, y, flip, model='gfx/bubble', state=0):
		super().__init__(x, y, 'gfx/bubble', settings.FLAG_PLAYER | settings.FLAG_FOE)
		self.flip = flip
		self.get_model().addFrameCallback('burst', 0, Bubble.rm)
		self.controller.addState(BubbleShoot())#(self.shoot)
		self.controller.addState(BubbleDrift())#self.drift)
		self.controller.addState(BubbleBurst())#Callback(self.burst)
		self.controller.setState(0)


	def burstAfterTimeout(self):
		self.controller.setState(2)

	def burstByPlayer(self):
		self.controller.setState(2)

T = TypeVar("T")
class BubbleFoe(BubbleBase, Generic[T]):

	def __init__(self, x, y, cls: Type[T]):
		super().__init__(x, y, cls.bubbleModel, settings.FLAG_PLAYER)
		self.cls = cls
		self.controller.addState(BubbleShoot())#(self.shoot)
		self.controller.addState(BubbleDrift())#self.drift)
		self.controller.addState(BubbleBurst())#Callback(self.burst)
		self.controller.setState(1)

	def burstAfterTimeout(self):
		# create the foe
		z = self.cls(self.x, self.y, -1, pal='angry_zenchan')
		self.parent.add(z)
		self.remove()
		#self.controller.setState(2)

	def burstByPlayer(self):
		z = DeadFoe(self.x, self.y, self.cls.deadModel, self.cls.deadPal)
		self.parent.add(z)
		self.remove()


