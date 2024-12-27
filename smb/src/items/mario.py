import monkey
import settings


#from .items import Bubble
class MarioDead(monkey.ControllerState):
	"""This controller state is used for bonuses (e.g. mushrooms
	and 1up, when they move up from the bricks that originated them.
	"""
	def __init__(self):
		super().__init__()
		self.timer = 0
		self.vy = 150

	def init(self, node):
		self.g = self.node.controller.gravity
		self.ctrl = self.node.controller

	def start(self, **kwargs):
		print(kwargs)
		self.node.setAnimation('dead')
		self.node.collider.setMask(0)

	def update(self, dt):
		self.timer += dt
		if self.timer >= 0.5:
			self.vy -= self.g*dt
			self.node.move((0, self.vy * dt, 0))
			if self.timer >= 2.0:
				self.node.remove()
				monkey.close_room()
		pass
		#self.ctrl.move((0, 0.2), False)
		#if self.node.y > self.y0 + 16:
		#	self.node.controller.setState(1)


class Mario(monkey.Node):
	def on_hit_by_foe(self, player, foe, delta):
		print('HIT BY FOE', delta)
		self.setAnimation('dead')
		self.time = 0
		self.controller.setState(1)
		#player.remove()

	def changeMode(self, mode: int):
		if settings.state == mode:
			return
		settings.state = mode
		a = Mario(self.x, self.y)
		self.parent.add(a)
		self.remove()
		if mode == 0:
			# set invincibility
			a.invincible = True
			script=monkey.Script()
			script.add(monkey.actions.Blink(a.id,5, 0.2))
			script.add(monkey.actions.CallFunc(lambda : setattr(a, 'invincible', False)))


			monkey.play(script)

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
	def __init__(self, x, y, **kwargs):
		super().__init__()
		self.invincible = False

		state = settings.mario_states[settings.state]
		sprite = state['model']
		height = state['height']
		self.set_position(x, y, 1)
		batch = sprite[:sprite.find('/')]
		# add collider
		self.collider = monkey.components.Collider(settings.Flags.PLAYER,
											  settings.Flags.FOE, settings.Tags.PLAYER,
											  monkey.shapes.AABB(-6, 6, 0, height))
		self.add_component(self.collider)
		# add controller
		walk = kwargs.get('walk', 'walk')
		idle = kwargs.get('idle', 'idle')
		slide = kwargs.get('slide', 'idle')
		jumpUp = kwargs.get('jumpUp', 'jump')
		jumpDown = kwargs.get('jumpDown', 'jump')
		self.controller = monkey.components.PlayerController2D(batch, bounds=(-10,10,0,height), speed=100,
		 													   acceleration=500, jump_height=settings.jumpHeight, time_to_jump_apex=settings.timeToJumpApex,
		 													   walk=walk, idle=idle, slide=slide, jumpUp=jumpUp, jumpDown=jumpDown)
		self.controller.addModel(monkey.models.getSprite(sprite), idle, walk, slide, jumpUp, jumpDown)
		self.controller.addState(MarioDead())

		self.add_component(self.controller)
		self.controller.setState(0)
		self.add_component(monkey.components.Follow(0))








