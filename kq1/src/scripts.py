import monkey
import random
from . import item_builders
from . import settings
from . import utils

def retrieveFunc(f: list):
	if not f:
		return None
	if len(f) == 1:
		return globals()[f[0]]
	else:
		return globals()[f[0]](**f[1])

class CallFuncs:
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

def restart_room():
	monkey.close_room()

def history():
	print('sucalamerda',settings.last_action)
	if settings.last_action:
		monkey.get_node(settings.parser_id).setText(settings.last_action)

def goto_room(**kwargs):
	def f(hotspot, player):
		settings.previous_room = settings.room
		settings.room = kwargs.get('room')
		player = monkey.get_node(settings.player_id)
		x = kwargs.get('x', player.x)
		y = kwargs.get('y', player.y)
		dir = kwargs['dir']
		utils.moveTo('graham', settings.room, pos=[x,y], dir=dir)
		#settings.items['graham']['room'] = settings.room
		#settings.items['graham']['pos'] = [x, y]
		#settings.items['graham']['dir'] = dir
		monkey.close_room()
	return f

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
	for arg in kwargs['lines']:
		add_message_to_script(script, arg, **kwargs)
		#message(script, arg, **kwargs)
	monkey.play(script)


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


def addNode(node):
	monkey.get_node(settings.game_node_id).add(node)


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
			'ai_func': ['func_random', {'x0': 0, 'x1': 316, 'y0': 0, 'y1': 120}]
		}
		addNode(item_builders.character(alligator))


def push_rock(**kwargs):
	rock = kwargs['item']
	if rock.moved:
		msg(lines=[12])
	else:
		rock.moved = True
	# 	if is_within_bounds('rock'):
	# 		game_state.rock_moved = True
		script = monkey.Script()
		add_message_to_script(script, 13)
		script.add(monkey.actions.MoveBy(id=rock.iid, delta=(0, -12), time=1))
		#move_item_by('rock', (0, -12, 0))
		monkey.play(script)
	# 	else:
	# 		msg(id=93, x='rock')