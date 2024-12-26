import monkey
import settings

def makeScore(score):
	def f(node):
		node.remove()
		s = monkey.Node()
		s.set_model(monkey.models.getSprite(f'tiles/score_{score}'), batch='tiles')
		s.set_position(node.x, node.y, 2)
		m = monkey.components.Mover()
		m.add(monkey.actions.MoveBy(0, (0, 64), 2, 0,
			on_end=lambda node: node.remove()))
		s.add_component(m)
		node.parent.add(s)
		settings.score += score
		monkey.get_node(settings.id_label_score).updateText(f"{settings.score:06}")
	return f






def Text(**data):
	pos = data.get('pos', [0, 0])
	if 'id' in data:
		text = settings.strings[data['id']]
	else:
		text = data['text']
	t = monkey.Text('ui', 'mario', text)
	t.set_position(pos[0], pos[1], 0)
	return t

def Player(**data): #x, y, speed, acceleration, jh, tja):
	pos = data.get('pos', [0, 0])
	speed = data.get('speed')
	acceleration = data.get('acceleration', 0.1)
	jh = data.get('jump_height')
	tja = data.get('time_to_jump_apex')
	ms = settings.mario_states[settings.state]
	node = monkey.get_sprite(ms['model'])
	node.set_position(pos[0] * settings.tile_size, pos[1] * settings.tile_size, 0)
	node.add_component(monkey.components.Controller2D(size=ms['size'], batch='lines', label='controller2d', mask_up=2|16))
	node.add_component(monkey.components.SpriteCollider(
		settings.Flags.PLAYER, settings.Flags.FOE, settings.Tags.PLAYER, batch='lines'))
	cl = monkey.components.PlayerWalk2D(max_speed=speed,
    	acceleration=acceleration, jump_height=jh, time_to_jump_apex=tja)
	node.add_component(cl)
	node.add_component(monkey.components.Follow(0))

	def f():
		cl.setState(monkey.NodeState.INACTIVE)
	#node.addBehavior('warp', f)
	settings.player_id = node.id
	return node

class PrizeBrick(monkey.Node):

	def generateCoin(node):
		node.moving = False
		coin = monkey.Node()
		coin.set_model(monkey.models.getSprite('tiles/coin'), batch='tiles')
		coin.set_position(node.x, node.y, 2)
		m = monkey.components.Mover()
		m.add(monkey.actions.MoveAccelerated(0, (0, 120, 0),
		(0, -150, 0), y_min=node.y+16, on_end=makeScore(100)))
		coin.add_component(m)
		node.parent.add(coin)

	def generateBonus(node):
		node.moving = False

		from . import Bonus

		bonus = Bonus(pos=[node.x / 16 + 0.5, node.y / 16], z=2, model='mushroom', tag=settings.Tags.MUSHROOM)
		node.parent.add(bonus)


	def hit(self, player):
		if self.hitsLeft == 0 and not self.moving:
			return
		if not self.moving:
			self.hitsLeft -= 1
			if self.hitsLeft == 0:
				model = AnimatedTile(2,'tiles')
				self.set_model(model)
		self.mover.clear()
		self.mover.add(monkey.actions.MoveAccelerated(
			0, (0, 50, 0), (0, -150, 0), y_min=self.yMin,
			on_end=getattr(PrizeBrick, self.callback)))
		self.moving = True


	def __init__(self, **data):
		super().__init__()
		self.hitsLeft = data.get('hits', 1)
		self.moving = False
		pos = data['pos']
		z = data.get('z', 0)
		self.callback = data.get('callback')

		self.yMin = pos[1] * settings.tile_size
		self.set_position(pos[0] * settings.tile_size , pos[1] * settings.tile_size, z)
		model = AnimatedTile(1,'tiles')
		self.set_model(model)
		self.add_component(monkey.components.Collider(
			shape=monkey.shapes.AABB(0, settings.tile_size, 0, settings.tile_size),
			flag=2, mask=0, tag=0, batch='lines'))
		self.mover = monkey.components.Mover()
		# mover.add(monkey.actions.Move(0, p0, 0))
		# mover.add(monkey.actions.MoveBy(0, (0,100), 10))
		self.add_component(self.mover)
		sensor = monkey.Node()
		sensor.add_component (monkey.components.Collider(
			shape=monkey.shapes.AABB(4,12,-2,2),
			flag=settings.Flags.FOE,
			mask=settings.Flags.PLAYER,
			tag=settings.Tags.BRICK_SENSOR,
			batch='lines'
		))
		self.add(sensor)

class Brick(monkey.Node):
	"""A plain Mario brick block
	Mario can break the block only if he's Super
	"""
	def __init__(self, **data):
		super().__init__()
		pos = data['pos']
		z = data.get('z', 0)
		self.yMin = pos[1] * settings.tile_size
		self.set_position(pos[0] * settings.tile_size , pos[1] * settings.tile_size, z)
		model = AnimatedTile(3,'tiles')
		self.set_model(model)
		self.add_component(monkey.components.Collider(
			shape=monkey.shapes.AABB(0, settings.tile_size, 0, settings.tile_size),
			flag=2, mask=0, tag=0, batch='lines'))
		self.mover = monkey.components.Mover()
		self.add_component(self.mover)
		sensor = monkey.Node()
		sensor.add_component (monkey.components.Collider(
			shape=monkey.shapes.AABB(4,12,-2,2),
			flag=settings.Flags.FOE,
			mask=settings.Flags.PLAYER,
			tag=settings.Tags.BRICK_SENSOR,
			batch='lines'
		))
		self.add(sensor)

	def hit(self, player):
		if settings.state == 0:
			self.mover.clear()
			self.mover.add(monkey.actions.MoveAccelerated(
				0, (0, 50, 0), (0, -150, 0), y_min=self.yMin))
		else:
			self.remove()
			v = player.controller.velocity
			player.controller.velocity = (v[0], 0)

class Tiled(monkey.Node):
	def __init__(self, **data):
		super().__init__()
		pos = data['pos']
		z = data.get('z', 0)
		self.set_position(pos[0] * settings.tile_size , pos[1] * settings.tile_size, z)
		sheet = data.get('sheet', 'tiles')
		size = data.get('size', None)
		solid = data.get('solid', True)
		if 'tiled' in data:
			model = TileModel(data['tiled'], sheet)
		elif 'atiled' in data:
			model = AnimatedTile(data['atiled'], sheet)
		elif 'quad' in data and size:
			pal = data.get('pal', 0)
			quad = data.get('quad', None)
			model = monkey.models.Quad('tiles')
			model.add(quad, size=(quad[2] * size[0], quad[3] * size[1]), repeat=(size[0], size[1]), pal=pal)
		else:
			model = None
		if model:
			self.set_model(model)
		if size and solid:
			self.add_component(monkey.components.Collider(
				shape=monkey.shapes.AABB(0, size[0]*settings.tile_size, 0, size[1]*settings.tile_size),
				flag=2, mask=0, tag=0, batch='lines'))
			canMove = data.get('canMove', False)
			if canMove:
				mover = monkey.components.Mover()
				#mover.add(monkey.actions.Move(0, p0, 0))
				#mover.add(monkey.actions.MoveBy(0, (0,100), 10))
				self.add_component(mover)


def TileModel(name: str, sheet: str):
	tp = monkey.getTileParser(sheet)
	model = tp.parse(settings.data['models'][name])
	return model

def AnimatedTile(id: str, sheet: str):
	# make a animated tile model
	a = settings.data['animated_tiles'][id]
	size = a['size']
	frames = a.get('frames', 1)
	tpf = a['ticks_per_frame']
	scale = a.get('scale', 1)
	m1 = monkey.models.TileModel(sheet, size[0], size[1], frames, tpf, scale)
	for tile in a['tiles']:
		m1.addTile(tile['index'], tile.get('pal', 0), tile.get('fliph', False), tile.get('flipv', False))
	print(a['data'])
	for i in range(0, len(a['data']), 3):
		m1.setTile((a['data'][i]), (a['data'][i+1]), (a['data'][i+2]))
	return m1

def Platform(**data):
	size = data['size']
	pos = data['pos']
	quad = data.get('quad', None)
	z = data.get('z', 0)
	pal = data.get('pal', 0)
	solid = data.get('solid', True)
	node = monkey.Node()
	node.set_position(pos[0] * settings.tile_size , pos[1] * settings.tile_size, z)
	if quad:
		model = monkey.models.Quad('tiles')
		model.add(quad, size=(quad[2] * size[0], quad[3] * size[1]), repeat=(size[0], size[1]), pal=pal)
		node.set_model(model)
	if solid:
		node.add_component(monkey.components.Collider(
			shape=monkey.shapes.AABB(0, size[0]*settings.tile_size, 0, size[1]*settings.tile_size),
			flag=2, mask=0, tag=0, batch='lines'))
	return node
