import monkey
from .collision import MarioVsGoomba
from . import values


class GameRoom(monkey.Room):
	def __init__(self, camSize: tuple, worldSize: tuple, sheet: str):
		super().__init__()
		dw = camSize[0]
		dh = camSize[1]
		cam = monkey.CamOrtho(dw, dh,
							  viewport=(0, 0, dw, dh),
							  bounds_x=(dw//2, worldSize[0] - dw//2), bounds_y=(dh//2, worldSize[1] - dh//2))
		self.add_camera(cam)
		collision_engine = monkey.CollisionEngine2D(80, 80)
		collision_engine.addResponse(MarioVsGoomba(values.TAG_PLAYER, values.TAG_FOE))
		self.add_runner(collision_engine)
		root = self.root()
		kb = monkey.components.Keyboard()
		kb.add(299, 1, 0, lambda: monkey.close_room())
		root.add_component(kb)
		self.add_batch('lines', monkey.LineBatch(max_elements=800, cam=0))
		self.add_batch('gfx', monkey.SpriteBatch(max_elements=10000, cam=0, sheet=sheet))
		monkey.engine().setCurrentRoom(self)
		settings.bubinfo = rle_decode(li['bubble'])


class BubbleRoom(GameRoom):
	def __init__(self, camSize: tuple, worldSize: tuple, sheet: str):
		super().__init__(camSize, worldSize, sheet)
