import monkey2

from .. import state
from .. import assetman
from .. import scripts

def walk_player_to(pos, turn=None):
	script = monkey2.Script('__PLAYER')
	player = state.getNode('PLAYER')
	wa = state.getNode('WALKAREA_0')
	sched = state.getNode('SCHEDULER')
	script.addAction(monkey2.actions.Walk(player, wa, pos, state.PLAYER_SPEED), -1)
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
	main.setPosition([160, 100, 5])
	a = monkey2.Text('ui/sierra', s, (0,0,0,1), align=monkey2.Alignment.LEFT, width=state.TEXT_WIDTH, anchor=(0.5, 0.5))
	rect = scripts.makeRect(0, 0, a.size[0] + 2*state.TEXT_MARGIN_X, a.size[1]+ 2 *state.TEXT_MARGIN_Y,
	                        state.COLORS.WHITE, (0.5, 0.5), monkey2.ModelType.SOLID)
	rect2 = scripts.makeRect(0, 0, a.size[0] + 12, a.size[1] + 6, state.COLORS.RED, (0.5, 0.5), monkey2.ModelType.WIRE)
	rect3 = scripts.makeRect(0, 0, a.size[0] + 14, a.size[1] + 6, state.COLORS.RED, (0.5, 0.5), monkey2.ModelType.WIRE)
	main.add(rect)
	main.add(rect2)
	main.add(rect3)
	a.setPosition([0, 0, 0.1])
	main.add(a)
	return main


def take(**kwargs):
	item = kwargs['item']
	if item in state.inventory:
		message(text=10, env={'x': item})
	else:
		msg_ok = kwargs['ok']
		state.inventory[item] = 1
		message(text=msg_ok)




def message(**kwargs):
	id = kwargs.get('text')
	env = kwargs.get('env', None)
	text = scripts.eval_string(kwargs.get('text'), env)

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
	s.addAction(monkey2.actions.CallFunc(addNode(text)))
	s.addAction(monkey2.actions.WaitForMouseClick(pause(False), pause(True)))#setMainNodeActive(False)))
	s.addAction(monkey2.actions.CallFunc(rmNode(text.id)))


def gotoRoom(player, hotspot):
	print('SUCAMENO',hotspot.userData)
	state.room = hotspot.userData['room']
	x = hotspot.userData.get('x', player.x)
	y = hotspot.userData.get('y', player.y)
	state.PLAYER_POS = [x, y, 0]
	state.PLAYER_DIR = hotspot.userData['dir']
	monkey2.closeRoom()


def drown(player, hotspot):
	s = monkey2.Script(state.PLAYER_SCRIPT_ID)
	pos = player.getPosition()
	args = hotspot.userData
	x = args.get('x', pos[0])
	y = args.get('y', pos[1])

	s.addAction(monkey2.actions.CallFunc(enableControls(False)))
	s.addAction(monkey2.actions.CallFunc(lambda: player.setPosition([x, y, 0])))
	s.addAction(monkey2.actions.Animate(player, 'drown'))
	s.addAction(monkey2.actions.Delay(2))
	#a = createText('Pino')
	#s.addAction(monkey2.actions.CallFunc(addNode(a)))
	addMessage(s,3)
	s.addAction(monkey2.actions.Delay(2))
	s.addAction(monkey2.actions.CallFunc(rmNode(state.IDS['PLAYER'])))
	addMessage(s, 4)
	monkey2.getNode(state.IDS['SCHEDULER']).play(s)
