import monkey
from . import settings


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
