import monkey
from . import values




class Mario(monkey.Node):
	def __del__(self):
		print('PANZONE',self.id)

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

	def __init__(self, x, y, sprite, width, height, **kwargs):
		super().__init__()
		#monkey.engine().storeRef(self)
		self.time=0
		self.vx=0
		self.vy=0
		#self.tag = 'Mario'
		self.set_position(x, y, 1)
		# model
		batch = sprite[:sprite.find('/')]
		self.set_model(monkey.models.getSprite(sprite), batch=batch)
		# add collider
		collider = monkey.components.Collider(values.FLAG_PLAYER, values.FLAG_FOE, values.TAG_PLAYER, monkey.shapes.AABB(-width//2, width//2, 0, height))
		#collider.setResponse(values.TAG_FOE, on_enter=self.on_hit_by_foe)
		self.add_component(collider)
		# add controller
		walk = kwargs.get('walk', 'walk')
		idle = kwargs.get('idle', 'idle')
		slide = kwargs.get('slide', 'slide')
		jumpUp = kwargs.get('jumpUp', 'jump')
		jumpDown = kwargs.get('jumpDown', 'jump')
		self.controller = monkey.components.PlayerController2D(size=(16, 16), speed=100,
			acceleration=500, jump_height=64, time_to_jump_apex=0.5,
			walk=walk, idle=idle, slide=slide, jumpUp=jumpUp, jumpDown=jumpDown)
		#self.controller.addCallback(self.dead)
		self.add_component(self.controller)


		self.add_component(monkey.components.Follow(0))








