import monkey
from . import values

class Mario(monkey.Node):
	def on_hit_by_foe(player, foe):
		player.remove()
	def __init__(self, x, y):
		super().__init__()
		self.set_position(x, y)
		# add collider
		collider = monkey.components.Collider(values.FLAG_PLAYER, values.FLAG_FOE, values.TAG_PLAYER, monkey.shapes.AABB(-8, 8, 0, 16))
		collider.setResponse(values.TAG_FOE, on_enter=Mario.on_hit_by_foe)
		self.add_component(collider)
		# add controller
		self.add_component(monkey.components.PlayerController2D(size=(16, 16), speed=100,
			acceleration=500, jump_height=128, time_to_jump_apex=1))
		self.add_component(monkey.components.Follow(0))








