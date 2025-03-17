import monkey2
from . import state
import random
from . import assetman
from . import code
import re

class InventoryHotSpot(monkey2.HotSpot):
	def __init__(self, key, node_id, shape, priority, camera):
		super().__init__(shape, priority, camera)
		self.node_id = node_id
		self.key = key
		#self.actions = data.get('actions', {})

	def onEnter(self):
		node = monkey2.getNode(self.node_id)
		if node:
			node.setMultiplyColor((1,0,0,1))

	def onLeave(self):
		node = monkey2.getNode(self.node_id)
		if node:
			node.setMultiplyColor((0,0,0,1))

	def onClick(self, pos):
		self.node_id = -1
		monkey2.getNode(state.IDS['MOUSE_CTRL']).addAction(0, 4, self.key)
		exit_inventory()

def walk_to(s: monkey2.Script, pos, dir):
	player = monkey2.getNode(state.IDS['PLAYER'])
	walkarea = monkey2.getNode(state.IDS['WALKAREA_0'])
	s.addAction(monkey2.actions.Walk(player, walkarea, pos, state.PLAYER_SPEED))
	if dir:
		d = dir if dir != 'w' else 'e'
		s.addAction(monkey2.actions.Animate(player, f"idle-{d}"))
		s.addAction(monkey2.actions.CallFunc(lambda: player.flipX(dir=='w')))


def eval_field(data, env=None):
	if isinstance(data, list):  # process each item in the list
		return [eval_field(item, env) for item in data]

	elif isinstance(data, dict):
		processed_dict = {}
		for key, value in data.items():
			processed_dict[key] = eval_field(value, env)
		return processed_dict

	elif isinstance(data, str):
		match = re.fullmatch(r"\{(.+?)\}", data)
		if match:
			try:
				return eval(match.group(1), env)  # Evaluate the expression
			except Exception as e:
				print(f"Error evaluating expression {match.group(1)}: {e}")
				return data  # Return unchanged if eval fails

	return data  # return original data if it's not a string, list or dict


def eval_string(id: int, env=None):
	"""
	Replaces `{expression}` in the template string with the evaluated result.

	Args:
		template (str): The string containing `{...}` expressions.
		env (dict, optional): A dictionary of variables to be used in evaluation.

	Returns:
		str: The transformed string with evaluated expressions.
	"""
	if env is None:
		env = {}

	s = assetman.strings[id]
	def eval_match(match):
		expr = match.group(1).strip()  # Extract the content inside `{...}`
		try:
			result = eval(expr, {"__builtins__": {}}, env)  # Secure eval
			return str(result)  # Convert everything to string
		except Exception as e:
			return f"[ERROR: {e}]"  # Handle errors gracefully

	pattern = re.compile(r"\{([^{}]+)\}")  # Match `{...}` without nesting
	return pattern.sub(eval_match, s)

def makeRect(x, y, w, h, color, anchor, style, z=0):
	rect = monkey2.shapes.Rect(w, h, anchor=anchor)
	rectModel = rect.toModel(style)
	n = monkey2.Node()
	n.setModel(rectModel, 4 if style==0 else 5)
	n.setPosition(monkey2.Vec3(x, y, z))
	n.setMultiplyColor(color)
	return n

def makeText(x, y, text, color, align, anchor, z=0):
	t = monkey2.Text('ui/sierra', text, color,
	                 align=align, anchor=anchor)
	t.setPosition((x, y, z))
	return t





def restart():
	monkey2.closeRoom()

def exit_inventory():
	if state.inventory_mode == 1:
		monkey2.getNode(state.IDS['GAME_ROOT']).active = True
		monkey2.getNode(state.IDS['MOUSE_CTRL']).activateCamera(0, True)
		monkey2.getNode(state.IDS['INVENTORY']).remove()
		monkey2.getNode(state.IDS['MOUSE_CTRL']).setSequence(0)

		state.inventory_mode = 0


def enter_inventory():
	if state.inventory_mode == 0:
		state.inventory_mode = 1
		parent = monkey2.getNode(state.IDS['UI_ROOT'])

		monkey2.getNode(state.IDS['GAME_ROOT']).active = False
		monkey2.getNode(state.IDS['MOUSE_CTRL']).activateCamera(0, False)
		monkey2.getNode(state.IDS['MOUSE_CTRL']).setSequence(1)

		inventory_window = monkey2.Node()
		inventory_window.setPosition([160, 100, state.Z_TEXT])
		parent.add(inventory_window)
		inventory_window.add(makeRect(0, 0, 200, 120, state.COLORS.WHITE, (0.5, 0.5), monkey2.ModelType.SOLID))
		inventory_window.add(makeText(0, 60, "You're carrying:", (0,0,0,1), monkey2.Alignment.CENTER, (0,0), z=0.1))
		i = 52
		for key, value in state.inventory.items():
			if value > 0:
				text =makeText(-100, i, key, (0,0,0,1), monkey2.Alignment.LEFT, (0, 0),z=0.1)
				shape = monkey2.shapes.Rect(200, 8, anchor=(0,1))
				text.addComponent(InventoryHotSpot(key, text.id, shape, 0, 1))
				mm = monkey2.Node()
				model = shape.toModel(monkey2.ModelType.WIRE)
				mm.setModel(model, 4)
				mm.setMultiplyColor((1,0,0,1))
				text.add(mm)
				inventory_window.add(text)
				i -=8
		state.IDS['INVENTORY'] = inventory_window.id

def on_right_click(a: str):
	print(f'setting action = {a}')
	state.action = a

def on_left_click(camId: int, pos, action):
	print(f'click on {camId} at {pos}')
	if camId == 0 and action == 'walk':
		#print('fff')
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

