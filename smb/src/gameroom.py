import monkey
import settings
from . import items
from .mario import Mario
from .collision import PlayerVsBrick

class GameRoom(monkey.Room):
	def __init__(self):
		super().__init__()

		world = settings.worlds[settings.room]
		bg_color = world.get('bg_color', [0, 0, 0])
		world_size = world['size']
		self.set_clear_color(*bg_color)
		device_width = settings.device_size[0]
		device_height = settings.device_size[1]
		hdw = device_width // 2
		hdh = device_height // 2
		cam = monkey.CamOrtho(device_width, device_height,
		                      viewport=(0, 0, device_width, device_height),
		                      bounds_x=(hdw, world_size[0] - hdw), bounds_y=(hdh, world_size[1] - hdh))
		cam_ui = monkey.CamOrtho(device_width, device_height,
		                         viewport=(0, 0, device_width, device_height),
		                         bounds_x=(hdw, hdw), bounds_y=(hdh, hdh))
		self.add_camera(cam)
		self.add_camera(cam_ui)
		ce = monkey.CollisionEngine2D(80, 80)
		ce.addResponse(PlayerVsBrick(settings.Tags.PLAYER, settings.Tags.BRICK_SENSOR))
		#collision_engine.addResponse(BubbleVsFoe(settings.TAG_BUBBLE, settings.TAG_FOE))


		self.add_runner(ce)
		self.add_runner(monkey.Scheduler())

		self.add_batch('tiles', monkey.SpriteBatch(max_elements=10000, cam=0, sheet='tiles'))
		self.add_batch('lines', monkey.LineBatch(max_elements=2000, cam=0))
		self.add_batch('ui', monkey.SpriteBatch(max_elements=1000, cam=1, sheet='tiles'))
		monkey.engine().setCurrentRoom(self)
		root = self.root()
		settings.id_main_node = root.id
		kb = monkey.components.Keyboard()
		kb.add(settings.Keys.restart, 1, 0, lambda: monkey.close_room())
		root.add_component(kb)

		# ui part
		ui = monkey.Node()
		ui.add(monkey.Text('ui', 'mario', 'MARIO', pos=(3*8, 26*8, 1)))
		scoreLabel = monkey.Text('ui', 'mario', f"{settings.score:06}", pos=(3 * 8, 25 * 8, 1))
		ui.add(scoreLabel)
		ui.add(monkey.Text('ui', 'mario', 'WORLD', pos=(144, 26 * 8, 1)))
		ui.add(monkey.Text('ui', 'mario', world['name'], pos=(152, 25 * 8, 1)))
		ui.add(monkey.Text('ui', 'mario', 'TIME', pos=(200, 26 * 8, 1)))
		coinLabel = monkey.Text('ui', 'mario', f"*{settings.coins:02}", pos=(96, 25 * 8, 1))
		ui.add(coinLabel)
		root.add(ui)


		start_pos = world['start_positions'][settings.start_position]
		root.add(Mario(32, 64, 'tiles/mario'))
		#root.add(item_builders.Player(pos=[start_pos[0], start_pos[1]], speed=200,
		#                              jump_height=96, time_to_jump_apex=0.5))


		# add all other items
		objs = world.get('items', [])
		for item in objs:
			type = item['type']
			f = getattr(items, type, None)
			if f:
				node = f(**item)
				root.add(node)

		# a = monkey.Node()
		# a.set_position(8,64,0)
		# #m1 = monkey.models.TileModel('tiles', 2, 2, 2, 50)
		# #m1.addTile(0, 0, False, False)
		# #m1.setTile(0, 0, 0)
		# m1 = monkey.models.TileModel('tiles', 1, 1, 4, 20)
		# m1.addTile(58, 0, False, False)
		# m1.addTile(58, 2, False, False)
		# m1.addTile(58, 3, False, False)
		# m1.setTile(0, 0, 0)
		# m1.setTile(0, 1, 1)
		# m1.setTile(0, 2, 2)
		# m1.setTile(0, 3, 1)
		# a.set_model(m1)
		# root.add(a)
