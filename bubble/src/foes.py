import monkey
from . import settings
import random

class ZenChan(monkey.Node):

	def jmpInit(self):
		self.setAnimation('prepare_jump')
		self.time = 0
		self.nf = 0

	def jmpInitUpdate(self, dt):
		self.time += dt
		if self.time > 0.2:
			self.flip_x = not self.flip_x
			self.time = 0
			self.nf += 1
		if self.nf > 5:
			self.setAnimation('idle')
			self.controller.setState(1)

	def jmpStart(self):
		self.vy = self.controller.jumpVelocity

	def jmpHorizontalStart(self):
		self.vy = self.controller.jumpVelocity * 0.5


	def jmp(self, dt):
		self.vy += -self.controller.gravity * dt
		self.controller.move((0, self.vy * dt), False)
		if self.controller.grounded:
			self.vy = 0
			self.controller.setState(0)

	def jmpHorizontal(self,dt ):
		self.vy += -self.controller.gravity * dt
		self.controller.move((1, self.vy * dt), False)
		if self.controller.grounded:
			self.vy = 0
			self.controller.setState(0)



	def updatePosition(self, dt):
		self.vy += -self.controller.gravity * dt
		vx = 1 if self.controller.grounded else 0
		self.controller.move((vx, self.vy * dt), False)
		if self.controller.left:
			self.flip_x = False
		elif self.controller.right:
			self.flip_x = True
		# if grounded...

		if self.controller.grounded:
			self.vy = 0
			ix = int((self.x - 16) // 8)
			iy = int(self.y // 8)

			if ix >= 0 and ix < 28:
				up = settings.jmp[iy][ix]
				if (up & 1 and self.player.y > self.y + 4 and random.random() < 0.01):
					print('j up at ',ix,iy)
					self.controller.setState(3)
				elif not self.flip_x and up & 2 and self.player.y > self.y - 2:
					self.controller.setState(2)
				elif self.flip_x and up & 4 and self.player.y > self.y - 2:
					self.controller.setState(2)
				#print('I am in ',ix,iy,up)
		# if player is above, then try to jump up -

		# if on edge, --> player above or equal: jump, otherwise fall


	def __init__(self, x, y, sprite, dir, **kwargs):
		super().__init__()
		self.time = 0
		self.vy = 0
		self.player = monkey.get_node(settings.id_player)
		self.dir = dir
		self.flip_x = dir < 0
		self.set_position(x, y, 1)
		# model
		batch = sprite[:sprite.find('/')]
		self.set_model(monkey.models.getSprite(sprite), batch=batch)
		# add collider
		collider = monkey.components.Collider(settings.FLAG_FOE,
			settings.FLAG_PLAYER | settings.FLAG_BUBBLE, settings.TAG_FOE,
			monkey.shapes.AABB(-8, 8, 0, 16))
		self.add_component(collider)
		# add controller
		self.controller = monkey.components.Controller2D(size=(16,16), speed=20, acceleration=500,
			jump_height=48, time_to_jump_apex=1)
		    #walk='walk', idle='walk', slide='walk', jumpUp='walk',
		    #jumpDown='walk')
		self.controller.addCallback(update=self.updatePosition)
		self.controller.addCallback(start=self.jmpStart, update=self.jmp)
		self.controller.addCallback(start=self.jmpHorizontalStart, update=self.jmpHorizontal)
		self.controller.addCallback(start=self.jmpInit, update=self.jmpInitUpdate)
		self.add_component(self.controller)
		self.controller.setState(0)
		#self.controller.addModel(monkey.models.getSprite(sprite), idle, walk, slide, jumpUp, jumpDown)
		#bf = monkey.models.getSprite('gfx/bub_fire')
		# add event when frame is 2
		#bf.addFrameCallback('default', 2, Bub.makeBubble)
		# add event when frame count resets to 0
		#bf.addFrameCallback('default', 0, Bub.resetModel)

# no need to follow, no scrolling
# self.add_component(monkey.components.Follow(0))