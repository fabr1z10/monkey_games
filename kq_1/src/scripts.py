import monkey2
from . import state
import random

def move_alligator(alligator: monkey2.Node):
	def f():
		walkarea = state.getNode('WALKAREA_1')
		sched = state.getNode('SCHEDULER')
		def alli():
			x = random.randint(0,316)
			y = random.randint(0,166)
			print(f'going to {x},{y}')
			script = monkey2.Script(f'script_{alligator.id}')
			script.addAction(monkey2.actions.Walk(alligator, walkarea, (x,y), 50), -1)
			script.addAction(monkey2.actions.CallFunc(alli), 0)
			sched.add(script)


		script = monkey2.Script()
		script.setLoop()
		script.addAction(monkey2.actions.CallFunc(alli), -1)
		script.addAction(monkey2.actions.Delay(5.0), 0)
		sched.add(script)
		print(alligator)
	return f

