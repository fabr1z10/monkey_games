import monkey2
from .. import state
from .. import assetman
from .. import builder

def create_node(id: str, x: float, y: float):
	def f():
		items = assetman.items[id].copy()
		items['pos'][0] = x
		items['pos'][1] = y
		print(items)
		node = builder.nodeBuilder(items)
		state.getNode('GAME_ROOT').add(node)

	return f



def change_room(room):
	def f():
		state.room = room
		monkey2.closeRoom()
	return f