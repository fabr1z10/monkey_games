import monkey2

sprites = None
rooms = {}


def makeSpriteNode(id: str, x, y, batchId: int, batch, z=0, dynamicDepth=False):
	m = monkey2.Node()
	m.setPosition([x, y, z])
	model = makeSprite(id, batchId, batch)
	m.setModel(model)
	if dynamicDepth:
		m.addComponent(monkey2.DepthScale(166, 0))
	return m


def makeSprite(id: str, batchId: int, batch):
	s = sprites[id]
	texId = batch.addTexture(s['file'])
	sprite = monkey2.Sprite(s['data'], batchId, texId)
	df = None
	for anim, frame in s['animations'].items():
		if df is None:
			df = anim
		for i in range(len(frame)):
			sprite.add(anim, i, frame[i], 10)
	sprite.defaultAnimation = df
	return sprite