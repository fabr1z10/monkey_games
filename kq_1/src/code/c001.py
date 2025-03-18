import monkey2
from .. import state
import random
from . import callfunc
from . import c000

def on_start_elf():
	sched = state.getNode('SCHEDULER')
	s = monkey2.Script()
	s.addAction(monkey2.actions.Delay(random.randint(0,5)))
	s.addAction(monkey2.actions.CallFunc(callfunc.create_node('elf',52,106)))
	c000.addMessage(s, 27)
	sched.play(s)

def talkelf(hotspot, **kwargs):
	ppos = state.getNode('PLAYER').getPosition()
	epos = hotspot.node.getPosition()
	d2 = (ppos.x - epos.x)**2 + (ppos.y - epos.y)**2
	sched = state.getNode('SCHEDULER')
	s = monkey2.Script()
	print(d2)
	if d2 < 500:
		c000.addMessage(s, 29)
		s.addAction(monkey2.actions.CallFunc(lambda: hotspot.node.remove()))
	else:
		c000.addMessage(s, 30)
	sched.play(s)



def go_random():
	pass

def random_move():
	x=random.randint(0, 316)
	y=random.randint(0,166)
	return monkey2.Vec2(x,y)


def suca():
	print('mERD')
def move_elf(elf: monkey2.Node, walkarea_id: int):
	def f():
		walkarea = state.getNode(f'WALKAREA_{walkarea_id}')
		sched = state.getNode('SCHEDULER')
		def alli():
			x = random.randint(0,316)
			y = random.randint(0,166)
			#print(f'going to {x},{y}')
			script = monkey2.Script(f'script_{alligator.id}')
			script.addAction(monkey2.actions.Walk(alligator, walkarea, (x,y), 50), -1)
			script.addAction(monkey2.actions.CallFunc(alli), 0)
			sched.play(script)


		script = monkey2.Script()
		script.setLoop()
		script.addAction(monkey2.actions.CallFunc(alli), -1)
		script.addAction(monkey2.actions.Delay(5.0), 0)
		sched.play(script)
	return f