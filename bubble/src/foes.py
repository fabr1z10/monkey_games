import monkey
from . import settings
import random
import math

class PrepareJump(monkey.ControllerState):
	def start(self):
		self.node.setAnimation('prepare_jump')
		self.time = 0
		self.nf = 0

	def update(self, dt):
		self.time += dt
		if self.time > 0.2:
			self.node.flip_x = not self.node.flip_x
			self.time = 0
			self.nf += 1
		if self.nf > 5:
			self.node.setAnimation('idle')
			self.node.controller.setState(1)

class Jump(monkey.ControllerState):
	def start(self):
		self.node.vy = self.node.controller.jumpVelocity

	def update(self, dt):
		self.node.vy += -self.node.controller.gravity * dt
		self.node.controller.move((0, self.node.vy * dt), False)
		if self.node.controller.grounded:
			self.node.vy = 0
			self.node.controller.setState(0)

class JumpHor(monkey.ControllerState):
	def start(self):
		self.node.vy = self.node.controller.jumpVelocity * 0.5

	def update(self, dt):
		self.node.vy += -self.node.controller.gravity * dt
		self.node.controller.move((1, self.node.vy * dt), False)
		if self.node.controller.grounded:
			self.node.vy = 0
			self.node.controller.setState(0)


class Fly(monkey.ControllerState):
	def start(self):
		self.fc = 0
		self.rot = 0

	def update(self, dt):
		self.fc += 1
		if self.fc > 20:
			self.fc = 0
			self.rot += 1
			if self.rot >= 4:
				self.rot = 0
			self.node.getRenderer().setAngle(self.rot * math.pi * 0.5)

		if self.node.vy <= -50:
			self.node.controller.setState(1)
		self.node.move((self.node.vx * dt, self.node.vy * dt, 0))
		if self.node.x >= 232 or self.node.x <= 24:
			self.node.vx *= -1
		if self.node.y <= 0:
			self.node.set_position(self.node.x, 320, 1)
		self.node.vy -= 100*dt

class Fall(monkey.ControllerState):
	def start(self):
		self.fc = 0
		self.rot = 0
	def update(self, dt):
		self.fc += 1
		if self.fc > 20:
			self.fc = 0
			self.rot += 1
			if self.rot >= 4:
				self.rot = 0
			self.node.getRenderer().setAngle(self.rot * math.pi * 0.5)
		self.node.controller.move((0, self.node.vy * dt), False)
		if self.node.controller.grounded:
			bonus = Bonus(self.node.x, self.node.y-8, 'gfx/banana')
			self.node.parent.add(bonus)
			self.node.remove()
			# create bonus


		if self.node.y <= 0:
			self.node.set_position(self.node.x, 320, 1)


class Walk(monkey.ControllerState):

	def init(self, node):
		self.g = self.node.controller.gravity
		self.ctrl = self.node.controller

	def update(self, dt):
		self.node.vy += -self.g * dt
		vx = 1 if self.ctrl.grounded else 0
		self.ctrl.move((vx, self.node.vy * dt), False)
		if self.ctrl.left:
			self.node.flip_x = False
		elif self.ctrl.right:
			self.node.flip_x = True
		# if grounded...
		if self.ctrl.grounded:
			self.node.vy = 0
			ix = int((self.node.x - 16) // 8)
			iy = int(self.node.y // 8)
			if ix >= 0 and ix < 28:
				up = settings.jmp[iy][ix]
				if (up & 1 and self.node.player.y > self.node.y + 4 and random.random() < 0.01):
					self.ctrl.setState(3)
				elif not self.node.flip_x and up & 2 and self.node.player.y > self.node.y - 2:
					self.ctrl.setState(2)
				elif self.node.flip_x and up & 4 and self.node.player.y > self.node.y - 2:
					self.ctrl.setState(2)

class DeadFoe(monkey.Node):
	def __init__(self, x, y, model, pal):
		super().__init__()
		self.vx = random.randint(150,  300)
		self.vx *= -1 if random.random() < 0.5 else 1
		self.vy = 250

		self.set_position(x, y, 1)
		self.set_model(monkey.models.getSprite(model), batch='gfx')
		self.setPalette(pal)
		collider = monkey.components.Collider(settings.FLAG_FOE,
			0, 0, monkey.shapes.AABB(-8, 8, -8, 8))
		self.add_component(collider)
		# add controller
		self.controller = monkey.components.Controller2D(size=(16,16), speed=20, acceleration=500,
			jump_height=48, time_to_jump_apex=1)
		# add states
		self.controller.addState(Fly())#addCallback(update=self.updatePosition)
		self.controller.addState(Fall())#addCallback(update=self.updatePosition)

		self.add_component(self.controller)
		self.controller.setState(0)


class ZenChan(monkey.Node):
	bubbleModel = 'gfx/zenchan_bubble'
	deadModel = 'gfx/zenchan_dead'
	deadPal ='dead_zenchan'

	def create_bubble(self):
		from .items import BubbleFoe
		bubble = BubbleFoe(self.x, self.y + 8, self.__class__)#False, model='gfx/zenchan_bubble',state=1)
		self.parent.add(bubble)

	def __init__(self, x, y, dir, **kwargs):
		super().__init__()
		pal = kwargs.get('pal', None)
		self.time = 0
		# vertical velocity - should be stored here as it keeps its value
		# across different states
		self.vy = 0
		# hold a reference to player -> we need to decide what to do
		self.player = monkey.get_node(settings.id_player)
		self.dir = dir
		self.flip_x = dir < 0
		self.set_position(x, y, 1)
		# model
		sprite = 'gfx/zenchan'
		batch = sprite[:sprite.find('/')]
		self.set_model(monkey.models.getSprite(sprite), batch=batch)
		if pal:
			self.setPalette(pal)
		# add collider
		collider = monkey.components.Collider(settings.FLAG_FOE,
			settings.FLAG_PLAYER | settings.FLAG_BUBBLE, settings.TAG_FOE,
			monkey.shapes.AABB(-8, 8, 0, 16))
		self.add_component(collider)
		# add controller
		self.controller = monkey.components.Controller2D(size=(16,16), speed=20, acceleration=500,
			jump_height=48, time_to_jump_apex=1)
		# add states
		self.controller.addState(Walk())#addCallback(update=self.updatePosition)
		self.controller.addState(Jump())
		self.controller.addState(JumpHor())
		self.controller.addState(PrepareJump())
		self.add_component(self.controller)
		self.controller.setState(0)

class Bonus(monkey.Node):
	def __init__(self, x, y, model):
		super().__init__()
		self.set_position(x, y, 1)
		self.set_model(monkey.models.getSprite(model), batch='gfx')
		# add collider
		collider = monkey.components.Collider(settings.FLAG_FOE,
			settings.FLAG_PLAYER, settings.TAG_BONUS,
			monkey.shapes.AABB(-8, 8, 0, 16))
		self.add_component(collider)
