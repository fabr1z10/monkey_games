import monkey
from . import values

class RectangularPlatform(monkey.Node):
	def __init__(self, x, y, tx, ty, width, height, tw=1, th=1):
		super().__init__()
		self.set_position(x, y)
		platform_width = width * tw * values.TILESIZE
		platform_height = height * th * values.TILESIZE
		tp= monkey.TileParser('gfx')
		self.set_model(tp.parse('Q {0},{1},{2},{3},{4},{5}'.format(tx, ty, tw, th, width, height)))
		self.add_component(monkey.components.Collider(values.FLAG_PLATFORM, 0, 1,
			monkey.shapes.AABB(0, platform_width, 0, platform_height)))




