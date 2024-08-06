import monkey
from . import settings
from . import engine
from . import data as dd
from . import scripts
from . import utils
from addict import Dict

def pippo(x,y):
	print('figga')






def build(data):
	itemType = data['type']
	settings.monkeyAssert(itemType in globals(), "Unknown builder: " + itemType)
	builder = globals()[itemType]#, None)
	node = builder(data)
	#print('figa',data,type(data), isinstance(data,AttrDict))
	#if isinstance(data, AttrDict):
	#	print('sucalo',node.id)
	#		data.iid = node.id
	#print('figa',data,type(data), isinstance(data,AttrDict))

	return node

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

def node(data):
	n = monkey.Node()
	pos = utils.read(data, 'pos', [0, 0, 0])#data.get('pos', [0, 0, 0])
	auto_depth = data.get('auto_depth', False)
	z = pos[2] if not auto_depth else 1.0 - pos[1] / 166.0
	n.set_position(pos[0], pos[1], z)
	baseline = data.get('baseline', None)
	if baseline:
		n.add_component(monkey.components.Baseline(monkey.shapes.PolyLine(baseline)))
	hole = data.get('hole', None)
	if hole:
		mode = hole.get('mode', 'all')
		s, m = utils.readShape(hole)
		if isinstance(s, monkey.shapes.PolyLine):
			dd.walkArea.addLinearWall(m, [pos[0], pos[1]])
		else:
			dd.walkArea.addPolyWall(m, [pos[0], pos[1]])
		if mode == 'all':
			n.add_component(monkey.components.Collider(2, 0, 0, s, batch='lines'))
		if 'collide' in hole:
			collider = utils.makeCollider(hole['collide'], shape=s)
			n.add_component(collider)
	collider = data.get('collider', None)
	if collider:
		collider = utils.makeCollider(data['collide'])
		n.add_component(collider)
	if 'quad' in data:
		batchId = data['quad']['batch']
		room =monkey.engine().getRoom()
		if not room.hasBatch(batchId):
			room.add_batch(batchId, monkey.SpriteBatch(max_elements=10000, cam=0, sheet=batchId))
		a = monkey.models.Quad(batchId)
		a.add(data['quad']['coords'])
		n.set_model(a)
	elif 'sprite' in data:
		spr=data['sprite']
		batchId = spr[:spr.find('/')]
		n.set_model(monkey.models.getSprite(data['sprite']), batch=batchId)
	return n



# this function creates a function generating a foe following player. You can specify the initial position,
# the speed, the sprite and the callback function to call if the foe catches the player
# def create_foe(id: str, sprite: str, x: float, y: float, speed: float, callback: str, msg: int, **kwargs):
# 	def f():
#         # if anim_dir is True, the sprites need to h
#         anim_dir = kwargs.get('anim_dir', True)
#         flip_horizontal = kwargs.get('flip_horizontal', True)
#         func_ai = kwargs.get('func_ai', func_follow_player)
#         call_every = kwargs.get('period', 1)
#         on_create = kwargs.get('on_create', None)
#         a = monkey.get_sprite(sprite)
#         a.set_position(x, y, 0)
#         walk_anim= kwargs.get('walk_anim', 'walk')
#         idle_anim = kwargs.get('idle_anim', 'walk')
#         a.add_component(monkey.components.NPCSierraFollow(func_ai, speed, call_every, z_func=settings.z_func,
#             anim_dir=anim_dir, walk_anim=walk_anim, idle_anim=idle_anim, flip_horizontal=flip_horizontal))
#         collide = kwargs.get('collider', False)
#         if collide:
#             flag = kwargs.get('flag', settings.CollisionFlags.foe)
#             mask = kwargs.get('mask', settings.CollisionFlags.player)
#             collider = monkey.components.Collider(flag, mask, 1, monkey.shapes.AABB(-5, 5, -1, 1), batch='lines')
#             if callback:
#                 collider.setResponse(0, on_enter=globals()[callback])
#             #if callback:
#             #    a.user_data = {
#             #        'on_enter': [callback]
#             #    }
#             a.add_component(collider)
#
#         game_state.nodes[id] = a.id
#         monkey.get_node(game_state.Ids.game_node).add(a)
#         if msg != -1:
#             s = monkey.Script()
#             message(s, msg)
#             monkey.play(s)
#         if on_create:
#             monkey.play(on_create)
#
#     return f

def character(data):
	print(data)
	assert 'speed' in data
	sprite = data['sprite']
	batchId = sprite[:sprite.find('/')]
	room = monkey.engine().getRoom()
	if not room.hasBatch(batchId):
		print(' -- adding batch:',batchId)
		room.add_batch(batchId, monkey.SpriteBatch(max_elements=10000, cam=0, sheet=batchId))
	b = monkey.get_sprite(sprite)
	pos = data.get('pos', [0, 0, 0])
	isPlayer = data.get('is_player', False)
	z = 1.0 - pos[1] / 166.0
	b.set_position(pos[0], pos[1], z)
	speed = data['speed']
	print('HEY SPEED',speed, 'speed' in data)
	direction = data.get('dir', 'e')
	#b = monkey.get_sprite('sprites/' + sprite)
	print('direction=',direction)
	if isPlayer:
		b.add_component(monkey.components.PlayerSierraController(half_width=2,
			speed=speed, skinWidth=1, dir=direction))
	else:
		# we need to have an ai function that moves the player
		func_ai = utils.retrieveFunc(data['ai_func'])
		walk_anim = data.get('walk_anim', 'walk')
		idle_anim = data.get('idle_anim', 'walk')
		call_every = data.get('period', 1)
		walk_area_id = data.get('walk_area', 0)
		anim_dir = data.get('anim_dir', True)
		flip_horizontal = data.get('flip_horizontal', True)
		b.add_component(monkey.components.NPCSierraFollow(func_ai, speed, call_every,
            anim_dir=anim_dir, walk_anim=walk_anim, idle_anim=idle_anim, flip_horizontal=flip_horizontal, walk_area=walk_area_id))

	# setup collider
	flag = data.get('flag', settings.CollisionFlags.player if isPlayer else settings.CollisionFlags.foe)
	mask = data.get('mask', settings.CollisionFlags.foe | settings.CollisionFlags.hotspot if isPlayer else
		settings.CollisionFlags.player | settings.CollisionFlags.hotspot)
	tag = data.get('tag', 0 if isPlayer else 1)
	shape = monkey.shapes.AABB(-settings.collider_size[0], settings.collider_size[0], -settings.collider_size[1], settings.collider_size[1])
	collider = monkey.components.Collider(flag, mask, tag, shape, batch='lines')
	if 'response' in data:
		for response in data['response']:
			on_enter = utils.retrieveFunc(response.get('on_enter', []))
			on_exit = utils.retrieveFunc(response.get('on_exit', []))
			collider.setResponse(response['tag'], on_enter=on_enter, on_exit=on_exit)

	b.add_component(collider)

	#b.scale=scale
	if isPlayer:
		settings.player_id = b.id
	return b


def hotspot(data):
	node = monkey.Node()
	shape = monkey.shapes.AABB(*data['aabb'])
	collider = monkey.components.Collider(settings.CollisionFlags.hotspot, settings.CollisionFlags.player, 10,
		shape, batch='lines')
	node.add_component(collider)
	collider.setResponse(settings.CollisionTags.player,
		on_enter=utils.retrieveFunc(data.get('on_enter')),
		on_exit=utils.retrieveFunc(data.get('on_exit')),
		on_continue=utils.retrieveFunc(data.get('on_continue')))
	return node

def swim_area(data):
	return node({
		'type': 'node',
        'hole': {
			'poly': data.get('poly'),
        	'mode': 'npc',
        	'collide': {'response': [{'tag': 0, 'on_enter': 'start_swim', 'on_exit': 'end_swim'}]}
		}
	})

def bgitem(data):
	pos = data['pos']
	bl = data['baseline']
	#maxy = max (bl[i] for i in range(1, len(bl), 2))
	p = bl.copy()
	p.extend([p[-2], data['y_back'], p[0], data['y_back']])
	return node({
		'type': 'node',
		'quad': {'batch': data['batch'], 'coords': data['coords']},
		'auto_depth': True,
		'pos': [pos[0], pos[1], 0],
		'baseline': data['baseline'],
		'hole': {'poly': p}
	})

# - type: node
#        pos: [128, 41, 0]
#        quad:
#          batch: "cliff"
#          coords: [1,168,46,19]
#        auto_depth: True
#        baseline: [0,5,18,0,26,3,40,3,46,5]
#        hole:
#          poly: [0,5,18,0,26,3,40,3,46,5,46,7,0,7]




def lnk(data, aabb, x=None, y=None, dir=None):
	d = {
		'aabb': aabb,
		'on_enter': ['goto_room_hotspot', {
			'room': data['room'],
			'dir': data.get('dir', dir),
			'x_bounds': data.get('x_bounds', None),
			'y_bounds': data.get('y_bounds', None)
		}]
	}
	x = data.get('x', x)
	y = data.get('y', y)
	if x:
		d['on_enter'][1]['x'] = x
	if y:
		d['on_enter'][1]['y'] = y
	return hotspot(d)

def south(data):
	return lnk(data,[0, 316, 0, 2 * settings.collider_size[0]], y=120 - 10 * settings.collider_size[0], dir='s')

def north(data):
	return lnk(data, [0, 316, 120, 120 + 2*settings.collider_size[0]], y=10*settings.collider_size[0], dir='n')

def west(data):
	return lnk(data, [0, 2 * settings.collider_size[0], 0, 166], x=316 - 10*settings.collider_size[0], dir='w')

def east(data):
	return lnk(data, [316 - 2 * settings.collider_size[0], 316, 0, 166], x=10*settings.collider_size[0], dir='e')
