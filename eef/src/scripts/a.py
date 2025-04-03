import monkey2
import mupack

# a script can be interrupted, in this case we might have to do cleanup
# for instance, if we created
def play(s):
	sched = mupack.get_tag('SCHEDULER')
	sched.play(s)

# walk to an object
def walkScript(script, char_id, object_id):
	mupack.m_assert(object_id in mupack.assets.items, f"Unknown object: {object_id}")
	walk_to = mupack.assets.items[object_id].get('walk_to')
	mupack.m_assert(walk_to, f"Object {object_id} doesn't have <walk_to> property.")
	character = mupack.get_tag(char_id)
	wa = mupack.get_tag('WALKAREA_0')
	script.addAction(monkey2.actions.Walk(character, wa,
		monkey2.Vec2(walk_to[0], walk_to[1]),
		mupack.assets.state._player_speed))
	dir = walk_to[2]
	if dir == 'w':
		dir = 'e'
		script.addAction(monkey2.actions.CallFunc(lambda: character.flipX(True)))
	script.addAction(monkey2.actions.Animate(character, f"idle-{dir}"))

def addNode(node, parent):
	def f():
		parent.add(node)
		s = monkey2.Script()
		s.addAction(monkey2.actions.Delay(2))
		s.addAction(monkey2.actions.CallFunc(rmNode(node.id)))
		play(s)
	return f

def rmNode(id):
	def f():
		monkey2.getNode(id).remove()
	return f

def talkDynamic(node, anim):
	def f():
		d = node.animation[-1]
		node.animation = f'{anim}-{d}'
	return f

def say(script, char_id, msg):
	#script = monkey2.Script('__PLAYER')
	#character = mupack.get_tag(char_id)
	item = mupack.assets.items[char_id if char_id != 'PLAYER' else mupack.assets.state.player]
	text = monkey2.Text('uimain/c64',
		mupack.eval_string(msg),
		monkey2.Color(item['text_color']))
	character = mupack.get_tag(char_id)
	text.setPosition(monkey2.Vec3(2, 200, 0))
	script.addAction(monkey2.actions.CallFunc(addNode(text, mupack.get_tag('UI_ROOT'))))
	script.addAction(monkey2.actions.CallFunc(talkDynamic(character, 'talk')))
	script.addAction(monkey2.actions.Delay(2))
	script.addAction(monkey2.actions.CallFunc(talkDynamic(character, 'idle')))
	#script.addAction(monkey2.actions.CallFunc(rmNode(text.id)))


def on_left_click(camId: int, pos, action):
	#print(f'click on {camId} at {pos.x}, {pos.y}')
	if camId == 0:
		script = monkey2.Script('__PLAYER')
		player = mupack.get_tag('PLAYER')

		wa = mupack.get_tag('WALKAREA_0')
		sched = mupack.get_tag('SCHEDULER')
		print(' -- player is ', player.id, ' ', wa.id, ' ' , sched.id)
		#print(player,wa,pos,state.PLAYER_SPEED)
		print(type(mupack.assets.state._player_speed))
		script.addAction(monkey2.actions.Walk(player, wa, pos, mupack.assets.state._player_speed))#player, wa, pos, state.PLAYER_SPEED))
		#script.addAction(monkey2.actions.Animate(player, f"idle-s"))
		#if turn:
		#		script.addAction(monkey2.actions.Animate(player, f"idle-{turn}"), 0)
		sched.play(script)

def _walkto(o1, _):
	sched = mupack.get_tag('SCHEDULER')
	script = monkey2.Script('__PLAYER')
	walkScript(script, 'PLAYER', o1)
	sched.play(script)

def walkAndSay(item, string_id):
	script = monkey2.Script('__PLAYER')
	walkScript(script, 'PLAYER', item)
	say(script, 'PLAYER', string_id)
	sched = mupack.get_tag('SCHEDULER')
	sched.play(script)



def _read(o1, _):
	walkAndSay(o1, 22)

def _open(o1, _):
	walkAndSay(o1, 24)

def _close(o1, _):
	walkAndSay(o1, 25)