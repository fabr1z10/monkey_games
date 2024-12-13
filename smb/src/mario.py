import monkey
from . import settings
#from .items import Bubble

class Mario(monkey.Node):
	def on_hit_by_foe(self, player, foe, delta):
		print('HIT BY FOE', delta)
		self.setAnimation('dead')
		self.time = 0
		self.controller.setState(1)
		#player.remove()

	def bounceOnFoe(self):
		v = self.controller.velocity
		self.controller.velocity = (v[0], -v[1])

	def dead(self, dt):
		self.time += dt
		if self.time < 0.5:
			self.vy = 100
		elif self.time < 2.0:
			self.vy -= 50 * dt
			self.move((0, self.vy * dt, 0))
		else:
			self.remove()

	def fire(self):
		print('FIRE!')
		self.controller.setModel(1)

	def bounce(self):
		v = self.controller.velocity
		self.controller.velocity = (v[0], self.controller.jumpVelocity)

	def makeBubble(node):
		if node.can_bubble:
			bubble = Bubble(node.x, node.y + 8, node.flip_x)
			node.parent.add(bubble)

	def resetModel(node):
		node.controller.setModel(0)
	def __init__(self, x, y, sprite, **kwargs):
		super().__init__()
		width=16
		self.set_position(x, y, 1)
		batch = sprite[:sprite.find('/')]
		# add collider
		collider = monkey.components.Collider(settings.Flags.PLAYER,
			settings.Flags.FOE, settings.Tags.PLAYER,
			monkey.shapes.AABB(-8, 8, 0, 16))
		self.add_component(collider)
		# add controller
		walk = kwargs.get('walk', 'idle')
		idle = kwargs.get('idle', 'idle')
		slide = kwargs.get('slide', 'idle')
		jumpUp = kwargs.get('jumpUp', 'idle')
		jumpDown = kwargs.get('jumpDown', 'idle')
		self.controller = monkey.components.PlayerController2D(batch, size=(16, 16), speed=100,
			acceleration=500, jump_height=2, time_to_jump_apex=0.5,
			walk=walk, idle=idle, slide=slide, jumpUp=jumpUp, jumpDown=jumpDown)
		self.controller.addModel(monkey.models.getSprite(sprite), idle, walk, slide, jumpUp, jumpDown)
		# # add key event: when player hits key A, bub will create a bubble
		# self.controller.addKeyEvent(65, self.fire)
		self.add_component(self.controller)
		self.add_component(monkey.components.Follow(0))








