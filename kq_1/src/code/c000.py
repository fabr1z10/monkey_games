import monkey2

from .. import state
from .. import assetman

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
		print('FIFIFIFIFIFIFIFI')
		monkey2.getNode(state.IDS['GAME_ROOT']).add(node)
	return f

def rmNode(id: int):
	def f():
		monkey2.getNode(id).remove()
	return f
def createText(s: str):

	a = monkey2.Text('main/sierra', s, (0,0,0,1), align=monkey2.Alignment.LEFT, width=state.TEXT_WIDTH, anchor=(0.5, 0.5))
	rect = monkey2.shapes.Rect(a.size[0] + 2*state.TEXT_MARGIN_X, a.size[1]+ 2 *state.TEXT_MARGIN_Y, anchor=(0.5, 0.5))
	rectModel = rect.toModel((1,1,1,1), 1)
	rect2 = monkey2.shapes.Rect(a.size[0] + 2*6, a.size[1]+ 2 *3, anchor=(0.5, 0.5))
	rectModel2 = rect2.toModel(monkey2.fromHex('#AA0000'), 0)
	rect3 = monkey2.shapes.Rect(a.size[0] + 2*7, a.size[1]+ 2 *3, anchor=(0.5, 0.5))
	rectModel3 = rect3.toModel(monkey2.fromHex('#AA0000'), 0)
	main = monkey2.Node()
	main.setModel(rectModel, 3)
	main.setPosition([158, 83, 10])
	a.setPosition([0,0,0.1])
	main.add(a)
	b = monkey2.Node()
	b.setModel(rectModel2, 2)
	b.setPosition([0,0,0.1])
	main.add(b)
	b2 = monkey2.Node()
	b2.setModel(rectModel3, 2)
	b2.setPosition([0,0,0.1])
	main.add(b2)
	return main


def message(**kwargs):
	text = assetman.strings[kwargs.get('text')]

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
	state.room = 'garden_east'
	state.PLAYER_POS = [50, 50, 0]
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
