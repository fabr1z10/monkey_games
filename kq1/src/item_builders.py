import monkey
from . import settings
from . import engine
from . import data

def build(data):
	print(data)
	itemType = data['type']
	settings.monkeyAssert(itemType in globals(), "Unknown builder: " + itemType)
	builder = globals()[itemType]#, None)
	return builder(data)

def getShape(data):
	shape = None
	if 'poly' in data:
		poly = data['poly']
		shape = monkey.shapes.Polygon(poly)
	elif 'polyline' in data:
		polyline = data['polyline']
		shape = monkey.shapes.PolyLine(points=polyline)
	else:
		settings.monkeyAssert(shape, 'Shape not found!')
	return shape

def common(data):
	n = monkey.Node()
	pos = data.get('pos', [0, 0, 0])
	auto_depth = data.get('auto_depth', False)
	z = pos[2] if not auto_depth else 1.0 - pos[1] / 166.0
	n.set_position(pos[0], pos[1], z)
	walk_info = data.get('walk_info', None)
	if walk_info:
		# get nowalk area
		block = walk_info.get('block', None)
		baseline = walk_info.get('baseline', None)
		if block:
			n.add_component(monkey.components.Collider(2, 0, 0, getShape(block), batch='lines'))
		if baseline:
			n.add_component(monkey.components.Baseline(monkey.shapes.PolyLine(points=baseline)))

	return n

def bg(data):
	n = common(data)
	batchId = data['batch']
	room =monkey.engine().getRoom()
	if not room.hasBatch(batchId):
		room.add_batch(batchId, monkey.SpriteBatch(max_elements=10000, cam=0, sheet=batchId))
	a = monkey.models.Quad(batchId)
	a.add(data['quad'])
	n.set_model(a)
	return n

def character(data):
	sprite = data['sprite']
	batchId = sprite[:sprite.find('/')]
	room = monkey.engine().getRoom()
	if not room.hasBatch(batchId):
		print(' -- adding batch:',batchId)
		room.add_batch(batchId, monkey.SpriteBatch(max_elements=10000, cam=0, sheet=batchId))
	print('xxx')
	b = monkey.get_sprite(sprite)
	pos = data.get('pos', [0, 0, 0])
	isPlayer = data.get('is_player', False)
	z = 1.0 - pos[1] / 166.0
	b.set_position(pos[0], pos[1], z)
	speed = data['speed']
	#b = monkey.get_sprite('sprites/' + sprite)
	if isPlayer:
		b.add_component(monkey.components.PlayerSierraController(half_width=2, speed=speed,z_func=engine.z_func, skinWidth=1))
	print('cff')
	return b
	# setup collider
	flag = data.get('flag', settings.CollisionFlags.player if isPlayer else settings.CollisionFlags.foe)
	mask = data.get('mask', settings.CollisionFlags.foe if isPlayer else settings.CollisionFlags.player)
	tag = data.get('tag', 0 if isPlayer else 1)
	shape = monkey.shapes.AABB(-5, 5, -1, 1)
	collider = monkey.components.Collider(flag, mask, tag, shape, batch='lines')
	b.add_component(collider)

	#b.scale=scale
	if isPlayer:
		settings.player_id = sprite.id
	return sprite
