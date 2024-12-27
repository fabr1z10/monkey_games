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

	def __init__(self, flipOnEdge: bool, speed: float, flip: bool, anim: str = 'walk'):
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
		anim: str
			The animation to be played while walking. Defaults to 'walk'
		"""
		super().__init__()
		self.flipOnEdge = flipOnEdge
		self.flip = flip
		self.speed = speed
		self.anim = anim

	def init(self, node):
		self.g = self.node.controller.gravity
		self.ctrl = self.node.controller

	def start(self):
		self.node.setAnimation(self.anim)
		if self.flip:
			self.node.flip_x = True if self.node.dir == -1 else False
		else:
			self.node.flip_x = False

	def update(self, dt):
		k = -1 if (not self.flip and self.node.dir==-1) else 1
		#f = True if self.flip and self.dir==-1 else False
		self.node.vy += -self.g * dt
		self.ctrl.move((k * self.speed, self.node.vy * dt), False)
		if self.flip:
			self.node.flip_x = self.node.dir == -1
		if self.ctrl.left:
			self.node.dir = 1
		elif self.ctrl.right:
			self.node.dir = -1
		if self.ctrl.grounded:
			if self.flipOnEdge and self.ctrl.isFalling(k):
				self.node.dir = -self.node.dir
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

	def start(self, **kwargs):
		self.node.setAnimation(self.anim)
		self.node.collider.setMask(0)

	def update(self, dt):
		self.node.vy += -self.g * dt
		self.ctrl.move((0, self.node.vy * dt), False)
		self.timer += dt
		if self.timer >= self.timeout:
			self.node.remove()


class Sleep(monkey.ControllerState):
	def __init__(self, timeout1: float = 5, timeout2= 7,
		anim1: str = 'dead', anim2: str = 'restore'):
		"""
		Parameters
		----------
		timeout : float
			Time after which node is removed
		anim : str
			The animation played
		"""
		super().__init__()
		self.anim1 = anim1
		self.anim2 = anim2
		self.timeout1 = timeout1
		self.timeout2 = timeout2


	def init(self, node):
		self.g = self.node.controller.gravity
		self.ctrl = self.node.controller


	def p1(self):
		self.node.setAnimation(self.anim2)

	def p2(self):
		self.node.setAnimation('walk')
		self.node.controller.setState(0)

	def start(self, **kwargs):
		self.node.setAnimation(self.anim1)
		self.timer = 0
		self.actions = [ (self.timeout1, self.p1), (self.timeout2, self.p2) ]

	def update(self, dt):
		if self.actions:
			self.node.vy += -self.g * dt
			self.ctrl.move((0, self.node.vy * dt), False)
			self.timer += dt
			if self.timer >= self.actions[0][0]:
				self.actions[0][1]()
				self.actions.pop(0)

class Foe(monkey.Node):
	def __init__(self, **data):
		super().__init__()
		pos = data['pos']
		z = data.get('z', 1)
		self.set_position(pos[0] * settings.tile_size, pos[1] * settings.tile_size, z)
		pal = data.get('pal', None)
		self.vy=0
		# model
		self.dir = data.get('dir', -1)
		m = data.get('model')
		tag = data['tag']
		speed = data.get('speed', 0.5)
		height = data.get('height', 16)
		sprite = f'tiles/{m}'
		#batch = sprite[:sprite.find('/')]
		self.set_model(monkey.models.getSprite(sprite), batch='tiles')
		if pal:
			self.setPalette(pal)
		# add collider
		#self.collider = monkey.components.Collider(settings.Flags.FOE,
		#	settings.Flags.PLAYER, tag,
		#	monkey.shapes.AABB(-4, 4, 0, height))
		self.collider = monkey.components.SpriteCollider(settings.Flags.FOE,
		                                                 settings.Flags.PLAYER,
		                                                 tag)
		self.add_component(self.collider)
		# add controller
		self.controller = monkey.components.Controller2D(bounds=(-6,6,0,16),
			speed=speed, acceleration=500, jump_height=48, time_to_jump_apex=1)
		# add states
		self.controller.addState(Walk(True, speed,True))  # addCallback(update=self.updatePosition)
		self.add_component(self.controller)


class Goomba(Foe):
	def __init__(self, **data):
		super().__init__(model='goomba', speed=0.5, height=16, tag=settings.Tags.GOOMBA, **data)
		#self.controller.addState(Dead())
		self.controller.setState(0)

	def die(self):
		self.controller.setState(1)

class Koopa(Foe):
	def __init__(self, **data):
		super().__init__(model='koopa', speed=0.5, height=24, tag=settings.Tags.KOOPA, **data)
		self.controller.addState(Sleep())
		self.controller.addState(Walk(False, 3.0,
			False, 'dead'))  # addCallback(update=self.updatePosition)
		self.controller.setState(0)

	def die(self):
		self.controller.setState(1)


class Bonus(monkey.Node):
	def __init__(self, **data):
		super().__init__()
		self.dir = -1
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
		self.controller = monkey.components.Controller2D(bounds=(-8,8,0, 16), speed=20, acceleration=500,
			jump_height=48, time_to_jump_apex=1)
		# add states
		self.controller.addState(Rise())
		self.controller.addState(Walk(False, 0.5, False, 'idle'))  # addCallback(update=self.updatePosition)
		self.add_component(self.controller)
		self.controller.setState(0)