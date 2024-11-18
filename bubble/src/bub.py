import monkey
from . import settings
from .items import Bubble

class Bub(monkey.Node):
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

	def makeBubble(node):
		if node.can_bubble:
			bubble = Bubble(node.x, node.y + 8, node.flip_x)
			node.parent.add(bubble)

	def resetModel(node):
		node.controller.setModel(0)
	def __init__(self, x, y, sprite, width, height, **kwargs):
		super().__init__()
		self.can_bubble = True
		self.time=0
		self.vx=0
		self.vy=0
		#self.tag = 'Mario'
		self.set_position(x, y, 1)
		# model
		batch = sprite[:sprite.find('/')]
		#self.set_model(monkey.models.getSprite(sprite), batch=batch)
		# add collider
		collider = monkey.components.Collider(settings.FLAG_PLAYER,
			settings.FLAG_FOE | settings.FLAG_BUBBLE, settings.TAG_PLAYER,
			monkey.shapes.AABB(-width//2, width//2, 0, height))
		#collider.setResponse(values.TAG_FOE, on_enter=self.on_hit_by_foe)
		self.add_component(collider)
		# add controller
		walk = kwargs.get('walk', 'walk')
		idle = kwargs.get('idle', 'idle')
		slide = kwargs.get('slide', 'slide')
		jumpUp = kwargs.get('jumpUp', 'jump')
		jumpDown = kwargs.get('jumpDown', 'jump')
		self.controller = monkey.components.PlayerController2D(batch, size=(16, 16), speed=100,
			acceleration=500, jump_height=64, time_to_jump_apex=0.5,
			walk=walk, idle=idle, slide=slide, jumpUp=jumpUp, jumpDown=jumpDown)
		self.controller.addModel(monkey.models.getSprite(sprite), idle, walk, slide, jumpUp, jumpDown)
		bf = monkey.models.getSprite('gfx/bub_fire')
		# add event when frame is 2
		bf.addFrameCallback('default', 2, Bub.makeBubble)
		# add event when frame count resets to 0
		bf.addFrameCallback('default', 0, Bub.resetModel)

		self.controller.addModel(bf, 'default', 'default', 'default','default', 'default')
		# add key event: when player hits key A, bub will create a bubble
		self.controller.addKeyEvent(65, self.fire)

		self.add_component(self.controller)
		# no need to follow, no scrolling
		#self.add_component(monkey.components.Follow(0))








