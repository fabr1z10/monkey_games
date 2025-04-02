### build node
import monkey2
from monkey2 import Vec2, Vec3, Vec4, Color
import re
from . import assets
from . import settings
from . import lucas


from .util import add_tag, get_tag, exit_with_err



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

# create a node from yaml description
# source_item is a YAML node!!!
# we also want to convert field that depend on state
def nodeBuilder(key, source_item):
	item = eval_field(source_item, env={'item': source_item, 'state': assets.state})
	active = item.get('active', True)
	if not active:
		return None
	models = item.get('models', None)
	nodo = monkey2.Node() if models is None else monkey2.MultiSprite()
	pos = Vec3(item.get('pos', [0, 0, 0]))
	nodo.setPosition(pos)
	if models:
		for m in models['tree']:
			n = monkey2.Node()
			n.setModel(monkey2.getModel(m['model']))
			parent = m.get('parent', -1)
			slot = m.get('slot', 0)
			z = m.get('z', 0)
			nodo.addNode(n, parent, slot, z)
		for key, values in models['anims'].items():
			nodo.addAnimation(key, values)
	elif model := item.get('model', None):
		nodo.setModel(monkey2.getModel(model))
	if anim := item.get('anim', None):
		nodo.animation = anim

	if item.get('depth'):
		nodo.addComponent(monkey2.DepthScale(166, 0, settings.FLAG_WALK_BLOCK))


	if walk := item.get('walk', None):
		wareas = get_tag('WALKAREA_ROOT')
		if 'poly' in walk:
			data = walk['poly']
			shape = monkey2.shapes.Polygon(data)
		else:
			data = walk['lines']
			shape = monkey2.shapes.Polygon(data)
		for warea in wareas.getChildren():
			warea.addHole(data, nodo)
		nodo.addComponent(monkey2.Collider(shape, settings.FLAG_WALK_BLOCK, 0, 'block'))
	if hotspot := item.get('hotspot', None):
		a = monkey2.Node()
		# shape can be automatically generated or can be a rect
		if 'rect' in hotspot:
			rect = hotspot['rect']
			anchor = Vec2() if len(rect) == 2 else Vec2(rect[2], rect[3])
			shape = monkey2.shapes.Rect(rect[0], rect[1], anchor=anchor)
		# 	elif 'poly' in item['hotspot']:
		# 		shape = monkey2.shapes.Polygon(item['hotspot']['poly'])
		# 	else:
		# 		mm = model.split('/')
		# 		qq = assetman.quads[mm[1]]
		# 		shape = monkey2.shapes.fromImage(mm[0], qq['tex'], Vec4(qq['data']), 10)
		a.setModel(shape.toModel(monkey2.ModelType.WIRE), 2)
		a.setMultiplyColor(Color(1,0,0,1))
		hs = lucas.LucasObjectHotSpot(key, shape,
			hotspot.get('priority', 0), 0)
		nodo.addComponent(hs)
		nodo.add(a)
	# if cl := item.get('collider', None):
	# 	flag = cl['flag']
	# 	mask = cl['mask']
	# 	tag = cl['tag']
	# 	if 'poly' in cl:
	# 		shape = monkey2.shapes.Polygon(cl['poly'])
	# 	else:
	# 		rect = cl['rect']
	# 		anchor = monkey2.Vec2(rect[2], rect[3]) if len(rect) > 2 else monkey2.Vec2()
	# 		shape = monkey2.shapes.Rect(rect[0], rect[1], anchor)
	# 	nodo.addComponent(monkey2.Collider(shape, flag, mask, tag))
	# 	if oph := cl.get('on_player_hit'):
	# 		ce = monkey2.game().room().collisionEngine
	# 		ce.addResponse('player', tag, getattr(code, oph)())
	# 	sm = shape.toModel(monkey2.ModelType.WIRE)
	# 	ab = monkey2.Node()
	# 	ab.setModel(sm, 2)
	# 	nodo.add(ab)

	# if 'user_data' in item:
	# 	# print('USER=DATA=',item['user_data'])
	# 	if nodo.userData:
	# 		nodo.userData.update(item['user_data'])
	# 	else:
	# 		nodo.userData = item['user_data']
	# # print('FUCK',nodo.userData)
	# if 'npc' in item:
	# 	npc = item['npc']
	# 	walkAreaId = npc['walkarea']
	# 	walkArea = state.getNode(f"WALKAREA_{walkAreaId}")
	# 	refresh = npc['refresh']
	# 	speed = npc['speed']
	# 	onRefresh = getattr(code, npc['onRefresh'])
	# 	# onReach = getattr(code, npc['onReach'])
	# 	nodo.addComponent(monkey2.NPC(walkArea, refresh, speed, onRefresh))
	#
	# script = item.get('script', None)
	# if script:
	# 	fu = getattr(code, script, None)
	# 	if not fu:
	# 		exit_with_err(f"Cannot find script: {script}")
	# 	startUp.f.append(fu(nodo))
	# print('OK')
	return nodo