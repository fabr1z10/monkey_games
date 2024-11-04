import monkey
from . import values

class Mario(monkey.Node):
	def on_hit_by_foe(self, player, foe):
		self.setAnimation('dead')
		self.time = 0
		self.controller.setState(1)
		#player.remove()

	def dead(self, dt):
		self.time += dt
		if self.time < 0.5:
			self.vy = 100
		elif self.time < 2.0:
			self.vy -= 50 * dt
			self.move((0, self.vy * dt, 0))
		else:
			self.remove()

	def __init__(self, x, y):
		super().__init__()
		self.time=0
		self.vx=0
		self.vy=0
		#self.tag = 'Mario'
		self.set_position(x, y)
		# model
		self.set_model(monkey.models.getSprite('gfx/mario'), batch='gfx')
		# add collider
		collider = monkey.components.Collider(values.FLAG_PLAYER, values.FLAG_FOE, values.TAG_PLAYER, monkey.shapes.AABB(-8, 8, 0, 16))
		collider.setResponse(values.TAG_FOE, on_enter=self.on_hit_by_foe)
		self.add_component(collider)
		# add controller
		self.controller = monkey.components.PlayerController2D(size=(16, 16), speed=100,
			acceleration=500, jump_height=128, time_to_jump_apex=1)
		self.controller.addCallback(self.dead)
		self.add_component(self.controller)


		self.add_component(monkey.components.Follow(0))








