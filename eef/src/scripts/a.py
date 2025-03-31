import monkey2
import mupack

def on_left_click(camId: int, pos, action):
	print(f'click on {camId} at {pos.x}, {pos.y}')
	if camId == 0:
		script = monkey2.Script('__PLAYER')
		player = mupack.get_tag('PLAYER')
		wa = mupack.get_tag('WALKAREA_0')
		sched = mupack.get_tag('SCHEDULER')
		#print(player,wa,pos,state.PLAYER_SPEED)
		script.addAction(monkey2.actions.Walk(player, wa, pos, 10.0))#player, wa, pos, state.PLAYER_SPEED))
		#script.addAction(monkey2.actions.Animate(player, f"idle-s"))
		#if turn:
		#		script.addAction(monkey2.actions.Animate(player, f"idle-{turn}"), 0)
		sched.play(script)