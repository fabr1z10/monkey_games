import monkey
from .collision import MarioVsGoomba
from . import values


class GameRoom(monkey.Room):
	def __init__(self, worldSize: tuple):
		super().__init__()
		cam = monkey.CamOrtho(256, 240,
							  viewport=(0, 0, 256, 240),
							  bounds_x=(128, worldSize[0] - 128), bounds_y=(120, worldSize[1] - 120))
		self.add_camera(cam)
		collision_engine = monkey.CollisionEngine2D(80, 80)
		collision_engine.addResponse(MarioVsGoomba(values.TAG_PLAYER, values.TAG_FOE))
		self.add_runner(collision_engine)
		root = self.root()
		kb = monkey.components.Keyboard()
		kb.add(299, 1, 0, lambda: monkey.close_room())
		root.add_component(kb)
		self.add_batch('lines', monkey.LineBatch(max_elements=200, cam=0))
		self.add_batch('gfx', monkey.SpriteBatch(max_elements=10000, cam=0, sheet='1'))
		monkey.engine().setCurrentRoom(self)