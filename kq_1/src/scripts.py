import monkey2
from . import state
import random
from . import code




def on_right_click(a: str):
	print(f'setting action = {a}')
	state.action = a

def on_left_click(camId: int, pos):
	print(f'click on {camId} at {pos}')
	if camId == 0:
		code.walk_player_to(pos)
	# if state.target_object:
	# 	g = f"{state.action}_{state.target_object}"
	# 	print(f'Executing: {g}')
	# 	f = getattr(code, g, None)
	# 	if f:
	# 		f()


def move_alligator(alligator: monkey2.Node):
	def f():
		print('SUCA')
		walkarea = state.getNode('WALKAREA_1')
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
		print(alligator)
	return f

