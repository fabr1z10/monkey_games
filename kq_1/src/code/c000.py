import monkey2

from monkey2 import Vec3

from .. import state
from .. import assetman
from .. import scripts
from .. import util

def walk_player_to(pos, turn=None):
	print('calling walkplayer',turn, pos)
	script = monkey2.Script('__PLAYER')

	player = state.getNode('PLAYER')
	print('fresc',player.x)
	wa = state.getNode('WALKAREA_0')
	print(wa)
	sched = state.getNode('SCHEDULER')
	print(player,wa,pos,state.PLAYER_SPEED)
	#ww = monkey2.actions.Walk(player, wa, pos, state.PLAYER_SPEED)
	#aa = monkey2.actions.Walk( pos)
	script.addAction(monkey2.actions.Walk(player, wa, pos, state.PLAYER_SPEED))#player, wa, pos, state.PLAYER_SPEED))
	#script.addAction(monkey2.actions.Animate(player, f"idle-s"))
	if turn:
		script.addAction(monkey2.actions.Animate(player, f"idle-{turn}"), 0)
	sched.play(script)


def pause(value: bool):
	def f():
		monkey2.getNode(state.IDS['GAME_ROOT']).active = not value
	return f


def setMainNodeActive(value: bool):
	def f():
		monkey2.getNode(state.IDS['GAME_ROOT']).active = value
		monkey2.getNode(state.IDS['MOUSE_CTRL']).activateCamera(0, value)
	return f

def enableControls(value: bool):
	def f():
		monkey2.getNode(state.IDS['MOUSE_CTRL']).activateCamera(0, value)
	return f


def addText(id: int):
	def f():
		node = createText(assetman.strings[id])
		monkey2.getNode(state.IDS['GAME_ROOT']).add(node)
	return f


def addNode(node):
	def f():
		monkey2.getNode(state.IDS['UI_ROOT']).add(node)
	return f

def rmNode(id: int):
	def f():
		monkey2.getNode(id).remove()
	return f


def createText(s: str):
	main = monkey2.Node()
	main.setPosition(monkey2.Vec3(160, 100, 5))
	a = monkey2.Text(
		'ui/sierra',
		s,
		monkey2.Color(0, 0, 0, 1),
		align=monkey2.Alignment.LEFT,
		width=state.TEXT_WIDTH,
		anchor=monkey2.Vec2(0.5, 0.5))
	rect = scripts.makeRect(0, 0, a.size.x + 2*state.TEXT_MARGIN_X, a.size.y + 2 *state.TEXT_MARGIN_Y,
	                        state.COLORS.WHITE, monkey2.Vec2(0.5, 0.5), monkey2.ModelType.SOLID)
	rect2 = scripts.makeRect(0, 0, a.size.x + 12, a.size.y + 6, state.COLORS.RED, monkey2.Vec2(0.5, 0.5), monkey2.ModelType.WIRE)
	rect3 = scripts.makeRect(0, 0, a.size.x + 14, a.size.y + 6, state.COLORS.RED, monkey2.Vec2(0.5, 0.5), monkey2.ModelType.WIRE)
	main.add(rect)
	main.add(rect2)
	main.add(rect3)
	a.setPosition(monkey2.Vec3(0, 0, 0.1))
	main.add(a)
	return main

def change_room(room):
	def f():
		state.room = room
		monkey2.closeRoom()
	return f

def walk_door(hotspot, **kwargs):
	s = monkey2.Script(state.PLAYER_SCRIPT_ID)
	scripts.walk_to(s, monkey2.Vec2(hotspot.data['hotspot']['goto']), hotspot.data['hotspot'].get('dir', None))
	if hotspot.node.animation in ['open', 'opening']:
		s.addAction(monkey2.actions.CallFunc(change_room(kwargs['room'])))
	monkey2.getNode(state.IDS['SCHEDULER']).play(s)

def baseScript(hotspot):
	s = monkey2.Script(state.PLAYER_SCRIPT_ID)
	if 'goto' in hotspot.data['hotspot']:
		scripts.walk_to(s, monkey2.Vec2(hotspot.data['hotspot']['goto']), hotspot.data['hotspot'].get('dir', None))
	return s

def push_rock(hotspot, **kwargs):
	if hotspot.data['state'] == 1:
		message(hotspot, text=17)
	else:
		hotspot.data['state'] = 1
		s = baseScript(hotspot)
		addMessage(s, textId=18)
		s.addAction(monkey2.actions.MoveTo(hotspot.node, [236, 21], 10))
		monkey2.getNode(state.IDS['SCHEDULER']).play(s)


def toggle(hotspot, **kwargs):
	s = baseScript(hotspot)
	if hotspot.node.animation in ['open', 'opening']:
		s.addAction(monkey2.actions.Animate(hotspot.node,'closing'))
		hotspot.data['anim'] = 'closed'
	else:
		s.addAction(monkey2.actions.Animate(hotspot.node,'opening'))
		hotspot.data['anim'] = 'open'
	monkey2.getNode(state.IDS['SCHEDULER']).play(s)

def setActive(hotspot, value):
	hotspot.data['active'] = value

def take(hotspot, **kwargs):
	# default take
	print('ciao',hotspot.node.x)
	item = kwargs['item']
	if item in state.inventory:
		message(hotspot, text=10, env={'x': item})
	else:
		remove_on_pickup = kwargs.get('remove', True)
		s = baseScript(hotspot)
		msg_ok = kwargs['ok']
		state.inventory[item] = 1
		addMessage(s, msg_ok)
		if remove_on_pickup:
			s.addAction(monkey2.actions.CallFunc(lambda: hotspot.node.remove()))
			s.addAction(monkey2.actions.CallFunc(lambda: setActive(hotspot, False)))
		monkey2.getNode(state.IDS['SCHEDULER']).play(s)

		#message(text=msg_ok)




def message(hotspot, **kwargs):
	id = scripts.eval_field(kwargs.get('text'))
	env = kwargs.get('env', None)
	text = scripts.eval_string(id, env)

	# let's create a script that:
	# set game node inactive
	# show text
	s = monkey2.Script(state.PLAYER_SCRIPT_ID)
	#s.addAction(monkey2.actions.CallFunc(setMainNodeActive(False)), -1)
	textBox = createText(text)
	s.addAction(monkey2.actions.CallFunc(addNode(textBox)))
	s.addAction(monkey2.actions.WaitForMouseClick(setMainNodeActive(True), setMainNodeActive(False)))
	s.addAction(monkey2.actions.CallFunc(rmNode(textBox.id)))
	#s.addAction(monkey2.actions.CallFunc(), 3)
	monkey2.getNode(state.IDS['SCHEDULER']).play(s)

def nullo():
	return

def addMessage(s: monkey2.Script, textId: int):
	t = assetman.strings[textId]
	text = createText(t)
	# s.addAction(monkey2.actions.CallFunc(addNode(text)))
	# s.addAction(monkey2.actions.WaitForMouseClick(pause(False), pause(True)))#setMainNodeActive(False)))
	# s.addAction(monkey2.actions.CallFunc(rmNode(text.id)))
	s.addAction(monkey2.actions.CallFunc(addNode(text)))
	s.addAction(monkey2.actions.WaitForMouseClick(setMainNodeActive(True), setMainNodeActive(False)))
	s.addAction(monkey2.actions.CallFunc(rmNode(text.id)))

def gotoRoom(player, hotspot):
	print('SUCAMENO',hotspot.userData)
	state.room = hotspot.userData['room']
	x = hotspot.userData.get('x', player.x)
	y = hotspot.userData.get('y', player.y)
	state.PLAYER_POS = Vec3(x, y, 0)
	state.PLAYER_DIR = hotspot.userData['dir']
	monkey2.closeRoom()


def drown(player, hotspot):
	s = monkey2.Script(state.PLAYER_SCRIPT_ID)
	pos = player.getPosition()
	args = hotspot.userData
	print(hotspot.userData)

	x = args.get('x', pos.x)
	y = args.get('y', pos.y)

	s.addAction(monkey2.actions.CallFunc(enableControls(False)))
	s.addAction(monkey2.actions.CallFunc(lambda: player.setPosition(monkey2.Vec3(x, y, 0))))
	s.addAction(monkey2.actions.Animate(player, 'drown'))
	s.addAction(monkey2.actions.Delay(2))
	#a = createText('Pino')
	#s.addAction(monkey2.actions.CallFunc(addNode(a)))
	addMessage(s,3)
	s.addAction(monkey2.actions.Delay(2))
	s.addAction(monkey2.actions.CallFunc(rmNode(state.IDS['PLAYER'])))
	addMessage(s, 4)
	monkey2.getNode(state.IDS['SCHEDULER']).play(s)

def climb_tree(hotspot, **kwargs):
	s = baseScript(hotspot)
	addMessage(s, textId=24)
	state.room = 'treetop'
	state.PLAYER_POS = [85, 5, 0]
	state.PLAYER_DIR = 'n'
	s.addAction(monkey2.actions.CallFunc(lambda : monkey2.closeRoom()))
	monkey2.getNode(state.IDS['SCHEDULER']).play(s)