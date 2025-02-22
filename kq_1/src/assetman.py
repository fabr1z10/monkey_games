import monkey2

sprites = None
rooms = {}


def makeSpriteNode(id: str, x, y, batchId: int, batch, z=0, dynamicDepth=False,wa=None):
	m = monkey2.Node()
	m.setPosition([x, y, z])
	model = makeSprite(id, batchId, batch)
	m.setModel(model)
	if dynamicDepth:
		m.addComponent(monkey2.DepthScale(166, 0))
	if 'geometry' in sprites[id]:
		geom = sprites[id]['geometry']
		hole = geom.get('hole', 0)
		depth = geom.get('depth', 0)
		geoType = 0 if 'lines' in geom else 1
		points = geom['lines'] if geoType == 0 else geom['poly']
		if hole == 1:
			if geoType == 0:
				wa.addLine(points, m)
			else:
				wa.addHole(points, m)
		if depth == 1:
			if geoType == 0:
				shape = monkey2.shapes.PolyLine(points)
			else:
				shape = monkey2.shapes.Polygon(points)
			m.addComponent(monkey2.Collider(shape))
		print('SUCALAMERDA')
	return m


def makeSprite(id: str, batchId: int, batch):
	s = sprites[id]
	texId = batch.addTexture(s['file'])
	if 'animations' in s:
		sprite = monkey2.Sprite(s['data'], batchId, texId)
		df = None
		for anim, frame in s['animations'].items():
			if df is None:
				df = anim
			for i in range(len(frame)):
				sprite.add(anim, i, frame[i], 10)
		sprite.defaultAnimation = df
	else:
		sprite = monkey2.Quad(s['data'], batchId, texId)
	return sprite