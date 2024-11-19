import monkey
from . import settings

class ZenChan(monkey.Node):

	def x(self, dt):
		self.controller.move((1, 0), False)
		if self.controller.left:
			self.flip_x = False
		elif self.controller.right:
			self.flip_x = True
		# if player is above, then try to jump up

		# if on edge, --> player above or equal: jump, otherwise fall


	def __init__(self, x, y, sprite, dir, **kwargs):
		super().__init__()
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
			jump_height=128, time_to_jump_apex=1)
		    #walk='walk', idle='walk', slide='walk', jumpUp='walk',
		    #jumpDown='walk')
		self.controller.addCallback(self.x)
		self.add_component(self.controller)
		#self.controller.addModel(monkey.models.getSprite(sprite), idle, walk, slide, jumpUp, jumpDown)
		#bf = monkey.models.getSprite('gfx/bub_fire')
		# add event when frame is 2
		#bf.addFrameCallback('default', 2, Bub.makeBubble)
		# add event when frame count resets to 0
		#bf.addFrameCallback('default', 0, Bub.resetModel)

# no need to follow, no scrolling
# self.add_component(monkey.components.Follow(0))