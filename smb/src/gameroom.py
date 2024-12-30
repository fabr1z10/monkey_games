import monkey
import settings
from . import items

from .collision import PlayerVsBrick, PlayerVsMushroom, PlayerVsGoomba, \
	PlayerVsKoopa, PlayerVsHotspot, PlayerVsCoin, PlayerVsHotspotHor

def pairwise(iterable):
	"s -> (s0, s1), (s2, s3), (s4, s5), ..."
	a = iter(iterable)
	return zip(a, a)


class GameRoom(monkey.Room):
	def commonStart(self):
		print('FIGA22')
		settings.hotspot = None

	def __init__(self):
		super().__init__()
		self.addOnStart(self.commonStart)
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
		ce.addResponse(PlayerVsMushroom(settings.Tags.PLAYER, settings.Tags.MUSHROOM))
		ce.addResponse(PlayerVsGoomba(settings.Tags.PLAYER, settings.Tags.GOOMBA))
		ce.addResponse(PlayerVsKoopa(settings.Tags.PLAYER, settings.Tags.KOOPA))
		ce.addResponse(PlayerVsHotspot(settings.Tags.PLAYER, settings.Tags.HOTSPOT))
		ce.addResponse(PlayerVsCoin(settings.Tags.PLAYER, settings.Tags.COIN))
		ce.addResponse(PlayerVsHotspotHor(settings.Tags.PLAYER, settings.Tags.HOTSPOT_HOR))

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
		ui.add(monkey.Text('ui', 'mario', 'MARIO', pos=(3*8, 27*8, 1)))
		scoreLabel = monkey.Text('ui', 'mario', f"{settings.score:06}", pos=(3 * 8, 26 * 8, 1))
		ui.add(scoreLabel)
		ui.add(monkey.Text('ui', 'mario', 'WORLD', pos=(144, 27 * 8, 1)))
		ui.add(monkey.Text('ui', 'mario', world['name'], pos=(152, 26 * 8, 1)))
		ui.add(monkey.Text('ui', 'mario', 'TIME', pos=(200, 27 * 8, 1)))
		coinLabel = monkey.Text('ui', 'mario', f"*{settings.coins:02}", pos=(96, 26 * 8, 1))
		ui.add(coinLabel)
		ui.add(items.Tiled(pos=[5.5,12.5], atiled=0, sheet='ui'))


		settings.id_label_score = scoreLabel.id
		settings.id_label_coins = coinLabel.id
		root.add(ui)

		start_loc = world['start_positions'][settings.start_position]
		start_pos = start_loc['pos']
		onStart = start_loc.get('on_start', None)
		if onStart:
			self.addOnStart(getattr(items, onStart))
		mario = items.Mario(start_pos[0] * settings.tile_size, start_pos[1] * settings.tile_size)
		settings.id_player = mario.id
		root.add(mario)

		objs = world.get('items', [])
		for item in objs:
			type = item['type']
			f = getattr(items, type, None)
			if f:
				p = item.get('multi')
				if p:
					for x, y in pairwise(p):
						node = f(**item, pos=(x, y))
						root.add(node)
				else:
					node = f(**item)
					root.add(node)
