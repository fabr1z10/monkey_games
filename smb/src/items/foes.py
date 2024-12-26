import monkey
import settings

class Rise(monkey.ControllerState):
	"""This controller state is used for bonuses (e.g. mushrooms
	and 1up, when they move up from the bricks that originated them.
	"""
	def __init__(self):
		super().__init__()

	def init(self, node):
		self.ctrl = self.node.controller
		self.y0 = self.node.y
		self.node.flip_x = False

	def update(self, dt):
		self.ctrl.move((0, 0.2), False)
		if self.node.y > self.y0 + 16:
			self.node.controller.setState(1)

class Walk(monkey.ControllerState):

	def __init__(self, flipOnEdge: bool, speed: float, flip: bool, dir: int):
		"""
		Parameters
		----------
		flipOnEdge : bool
			Whether the character should turn direction at the
			end of the platform
		speed : float
			The character speed
		flip: bool
			True if sprite should be mirrored when walking left
		dir: int
			The initial direction, 1 for right, -1 for left
		"""
		super().__init__()
		self.flipOnEdge = flipOnEdge
		self.flip = flip
		self.speed = speed
		self.dir = dir

	def init(self, node):
		self.g = self.node.controller.gravity
		self.ctrl = self.node.controller
		if self.flip:
			self.node.flip_x = True if self.dir == -1 else False


	def update(self, dt):
		k = -1 if (not self.flip and self.dir==-1) else 1
		#f = True if self.flip and self.dir==-1 else False
		self.node.vy += -self.g * dt
		self.ctrl.move((k * self.speed, self.node.vy * dt), False)
		if self.flip:
			self.node.flip_x = self.dir == -1
		if self.ctrl.left:
			self.dir = 1
		elif self.ctrl.right:
			self.dir = -1
		if self.ctrl.grounded:
			if self.flipOnEdge and self.ctrl.isFalling(k):
				self.dir = -self.dir
			self.node.vy = 0

class Dead(monkey.ControllerState):
	def __init__(self, timeout: float = 5, anim: str = 'dead'):
		"""
		Parameters
		----------
		timeout : float
			Time after which node is removed
		anim : str
			The animation played
		"""
		super().__init__()
		self.anim= anim
		self.timeout = timeout
		self.timer = 0

	def init(self, node):
		self.g = self.node.controller.gravity
		self.ctrl = self.node.controller

	def start(self):
		self.node.setAnimation(self.anim)
		self.node.collider.setMask(0)

	def update(self, dt):
		self.node.vy += -self.g * dt
		self.ctrl.move((0, self.node.vy * dt), False)
		self.timer += dt
		if self.timer >= self.timeout:
			self.node.remove()


class Foe(monkey.Node):
	def __init__(self, **data):
		super().__init__()
		pos = data['pos']
		z = data.get('z', 1)
		self.set_position(pos[0] * settings.tile_size, pos[1] * settings.tile_size, z)
		pal = data.get('pal', None)
		self.vy=0
		# model
		m = data.get('model')
		speed = data.get('speed', 0.5)
		height = data.get('height', 16)
		sprite = f'tiles/{m}'
		#batch = sprite[:sprite.find('/')]
		self.set_model(monkey.models.getSprite(sprite), batch='tiles')
		if pal:
			self.setPalette(pal)
		# add collider
		self.collider = monkey.components.Collider(settings.Flags.FOE,
			settings.Flags.PLAYER, settings.Tags.GOOMBA,
			monkey.shapes.AABB(-4, 4, 0, height))
		self.add_component(self.collider)
		# add controller
		self.controller = monkey.components.Controller2D(size=(16, 16),
			speed=speed, acceleration=500, jump_height=48, time_to_jump_apex=1)
		# add states
		self.controller.addState(Walk(True, speed,
			True, -1))  # addCallback(update=self.updatePosition)
		self.add_component(self.controller)


class Goomba(Foe):
	def __init__(self, **data):
		super().__init__(model='goomba', speed=0.5, height=16, **data)
		self.controller.addState(Dead())
		self.controller.setState(0)

	def die(self):
		self.controller.setState(1)

class Koopa(Foe):
	def __init__(self, **data):
		super().__init__(model='koopa', speed=0.5, height=24, **data)
		self.controller.setState(0)


class Bonus(monkey.Node):
	def __init__(self, **data):
		super().__init__()
		pos = data['pos']
		z = data.get('z', 1)
		self.set_position(pos[0] * settings.tile_size, pos[1] * settings.tile_size, z)
		pal = data.get('pal', None)
		self.vy = 0
		model = data.get('model')
		tag = data.get('tag')
		self.set_model(monkey.models.getSprite(f'tiles/{model}'), batch='tiles')
		if pal:
			self.setPalette(pal)
		# add collider
		collider = monkey.components.Collider(settings.Flags.FOE,
			settings.Flags.PLAYER, tag,
		    monkey.shapes.AABB(-4, 4, 0, 16))
		self.add_component(collider)
		# add controller
		self.controller = monkey.components.Controller2D(size=(16, 16), speed=20, acceleration=500,
			jump_height=48, time_to_jump_apex=1)
		# add states
		self.controller.addState(Rise())
		self.controller.addState(Walk(False, 0.5, False, -1))  # addCallback(update=self.updatePosition)
		self.add_component(self.controller)
		self.controller.setState(0)