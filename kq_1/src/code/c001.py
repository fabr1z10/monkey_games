import monkey2
from .. import state
import random

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