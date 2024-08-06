import monkey
import random
from . import item_builders
from . import settings
from . import utils




def addNode(node):
	monkey.get_node(settings.game_node_id).add(node)


def create_foe_script(f):
	script = monkey.Script()
	script.add(monkey.actions.Delay(random.randint(1, 10)))
	script.add(monkey.actions.CallFunc(f))
	add_message_to_script(script, 24)
	monkey.play(script)




class CallFuncs:

	def _a(player, **kwargs):
		settings.previous_room = settings.room
		settings.room = kwargs.get('room')
		x = kwargs.get('x', player.x)
		y = kwargs.get('y', player.y)
		print('@@@@',kwargs)
		xb = kwargs.get('x_bounds', None)
		yb = kwargs.get('y_bounds', None)
		if xb:
			x = utils.clamp(x, xb[0], xb[1])
		if yb:
			y = utils.clamp(x, yb[0], yb[1])
		dir = kwargs.get('dir', 'e')
		utils.moveTo('graham', settings.room, pos=[x, y], dir=dir)
		monkey.close_room()



	def goto_room(**kwargs):
		def f():
			player = monkey.get_node(settings.player_id)
			CallFuncs._a(player, **kwargs)
		return f



	def set_main_node_active(value):
		def f():
			#monkey.get_node(settings.text_edit_node).active = value
			monkey.get_node(settings.game_node_id).state = value
			monkey.get_node(settings.parser_id).state = value
		return f

	def rm_node(*args):
		def f():
			for id in args:
				print('removing')
				monkey.get_node(id).remove()
			CallFuncs.set_main_node_active(monkey.NodeState.ACTIVE)()
		return f

	def add_node(node):
		def f():
			addNode(node)
		return f


def restart_room():
	monkey.close_room()

def history():
	print('sucalamerda',settings.last_action)
	if settings.last_action:
		monkey.get_node(settings.parser_id).setText(settings.last_action)

def goto_room_hotspot(**kwargs):
	def f(hotspot, player):
		CallFuncs._a(player, **kwargs)
	return f
#goto_room = CallFuncs.goto_room


def add_message_to_script(script, messageId, **kwargs):
	script.add(monkey.actions.CallFunc(function=CallFuncs.set_main_node_active(monkey.NodeState.PAUSED)))
	msg = utils.make_text(messageId, **kwargs)
	script.add(monkey.actions.Add(id=settings.text_node_id, node=msg))
	wk = monkey.actions.WaitForKey()
	wk.add(settings.Keys.enter, func=CallFuncs.rm_node(msg.id))
	script.add(wk)

# prints out a message
def msg(**kwargs):
	script = monkey.Script()
	if isinstance(kwargs['lines'], str) and kwargs['lines'][0] == '@':
		ccc = eval(kwargs['lines'][1:], {'items': settings.items})
	else:
		ccc = kwargs['lines']
	for arg in ccc:
		add_message_to_script(script, arg, **kwargs)
		#message(script, arg, **kwargs)
	monkey.play(script)

def look_hole(**kwargs):
	msg(lines=[15 if settings.items['rock'].moved else 14])


def fall2():
	player = monkey.get_node(settings.player_id)
	#player.set_position(177, 120, 0)
	z = 1.0 - 47.0/166.0
	script = monkey.Script()
	script.add(monkey.actions.SierraEnable(id=player.id, value=False))
	script.add(monkey.actions.CallFunc(lambda: player.set_position(177, 120, z)))
	script.add(monkey.actions.Animate(id=player.id, anim='fall'))
	script.add(monkey.actions.Move(id=player.id, position=(177, 47, z), speed=10))
	script.add(monkey.actions.Animate(id=player.id, anim='land'))
	add_message_to_script(script, 31)
	script.add(monkey.actions.Animate(id=player.id, anim='stars'))
	script.add(monkey.actions.Delay(5))
	script.add(monkey.actions.SierraEnable(id=player.id, value=True))

	monkey.play(script)


def fall(**kwargs):
	def f(hotspot, player):
		settings.on_room_start = fall2
		script = monkey.Script()
		add_message_to_script(script, 30)
		script.add(monkey.actions.SierraEnable(id=player.id, value=False))
		script.add(monkey.actions.CallFunc(lambda: player.set_position(player.x, player.y, -0.6)))
		script.add(monkey.actions.Animate(id=player.id, anim='fall'))
		script.add(monkey.actions.Move(id=player.id, position=(player.x, 0, -0.6), speed=10))
		script.add(monkey.actions.CallFunc(CallFuncs.goto_room('room_goldegg', x= 40, y=40)))
		#script.add(monkey.actions.CallFunc(CallFuncs.goto_room('room_goldegg', dir='s', x=200, y=50)))
		#script.add(monkey.actions.CallFunc(lambda: exit(1)))
		monkey.play(script)
	return f


def drown(**kwargs):
	def f(hotspot, player):
		x = kwargs.get('x', player.x)
		y = kwargs.get('y', player.y)
		script = monkey.Script()
		script.add(monkey.actions.SierraEnable(id=player.id, value=False))
		script.add(monkey.actions.Move(id=player.id, position=(x, y, 1 - y / 166), speed=0))
		script.add(monkey.actions.Animate(id=player.id, anim='drown'))
		monkey.play(script)

	return f





# moves character randomly in [»0, x1] x [y0, y1]
def func_random(**kwargs):
	def f():
		return random.randint(kwargs['x0'], kwargs['x1']), random.randint(kwargs['y0'], kwargs['y1'])
	return f


def init_start():
	for i in range(0, 2):
		alligator = {
			'type': 'character',
			'sprite': 'sprites/alligator',
			'speed': 30,
			'pos': [random.randint(10, 306), 2],
			'walk_area_id': 1,
			'ai_func': ['func_random', {'x0': 0, 'x1': 316, 'y0': 0, 'y1': 120}]
		}
		addNode(item_builders.character(alligator))

def init_ogre():
	def f():
		ogre = item_builders.character(settings.items.ogre)
		addNode(ogre)
	create_foe_script(f)


def push_rock(**kwargs):
	rock = kwargs['item']
	print('---',rock)
	if rock.moved:
		msg(lines=[12])
	else:
		rock.moved = True
		print('figa- --',rock.iid)
		script = monkey.Script()
		add_message_to_script(script, 13)
		script.add(monkey.actions.MoveBy(id=rock.iid, delta=(0, -12), time=1))
		script.add(monkey.actions.CallFunc(lambda: settings.wman.recomputeBaselines()))
		#move_item_by('rock', (0, -12, 0))
		monkey.play(script)
	# 	else:
	# 		msg(id=93, x='rock')

def add_to_inventory(**kwargs):
	item = kwargs['item']
	#print(kwargs['item'])
	# check if item is already held
	if item.name in settings.tree.find('graham'):
		# item is held
		msg(lines=[16])
	else:
		msg(lines=kwargs['lines'])
		settings.tree.find(item.name).move_to(settings.tree.find('graham'))
		node = monkey.get_node(item.iid)
		if node:
			node.remove()
		settings.tree.print()

def make_solid_rect(x, y, w, h, color = 'FFFFFF', z = 0):
	node = monkey.Node()
	node.set_model(monkey.models.from_shape('tri',
		monkey.shapes.AABB(0, w, 0, h),
		monkey.from_hex(color),
		monkey.FillType.Solid))
	node.set_position(x, y, z)
	return node

def make_outline_rect(x, y, w, h, color = 'FFFFFF', z = 0):
	node = monkey.Node()
	node.set_model(monkey.models.from_shape(
	'lines',
		monkey.shapes.AABB(0, w, 0, h),
		monkey.from_hex(color),
		monkey.FillType.Outline))
	node.set_position(x, y, z)
	return node

def make_outline2_rect(x, y, w, h, color='FFFFFF', z=0):
	node = monkey.Node()
	node.add(make_outline_rect(x, y, w, h, color, z))
	node.add(make_outline_rect(x+1, y, w-2, h, color, z))
	return node

def look_item(**kwargs):
	name = kwargs['item'].name
	if name in settings.tree.find('graham'):
		script = monkey.Script()
		#msg(lines=kwargs['held'])
		#idesc = settings.items['items'][item_id]['inventory']
		script.add(monkey.actions.CallFunc(function=CallFuncs.set_main_node_active(monkey.NodeState.PAUSED)))
		#msg = utils.make_text(kwargs['held'], **kwargs)
		#script.add(monkey.actions.Add(id=settings.text_node_id, node=msg))
		node = monkey.Node()
		node.add(utils.make_text(kwargs['held'][0], **kwargs))
		node.add(make_solid_rect(136, 0, 42, 47, color='000000', z=2))
		node.add(make_outline2_rect(136, 0, 42, 47, color='AA0000', z=2))
		spr = monkey.get_sprite(kwargs['image'])
		spr.set_position(157, 22, 3)
		node.add(spr)
		script.add(monkey.actions.Add(id=settings.text_node_id, node=node))
		wk = monkey.actions.WaitForKey()
		wk.add(settings.Keys.enter, func=CallFuncs.rm_node(node.id))
		script.add(wk)
		monkey.play(script)
	else:
		msg(lines=kwargs['not_held'])

def check_position(**kwargs):
	area = kwargs.get('area', None)
	if area:
		node = monkey.get_node(settings.items['graham'].iid)
		if node.x < area[0] or node.x > area[2] or node.y < area[1] or node.y > area[3]:
			msg(lines=[kwargs.get('outside_area_msg', 10)])
			return 1
	return 0

def climb_tree(**kwargs):
	m = check_position(**kwargs)
	if m == 0:
		n = monkey.Script()
		add_message_to_script(n, 23)
		n.add(monkey.actions.CallFunc(CallFuncs.goto_room('room_treetop', dir='n', x=82, y=5)))
		monkey.play(n)

def ciappi(ogre, player):
	player.remove()
	ogre.sendMessage(id="setFunc", func=None)
	ogre.setAnimation('catch')
	msg(lines=[25])

def start_swim(other, player):
	player.set_model(monkey.models.getSprite('sprites/graham_swim'), batch='sprites')

def end_swim(other, player):
	player.set_model(monkey.models.getSprite('sprites/graham'), batch='sprites')
