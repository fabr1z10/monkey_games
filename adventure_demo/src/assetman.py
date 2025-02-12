import monkey2

sprites = None

def makeSprite(id: str, batchId: int):
	print(sprites)
	s = sprites[id]
	sprite = monkey2.Sprite(s['data'], batchId)
	df = None
	for anim, frame in s['animations'].items():
		if df is None:
			df = anim
		for i in range(len(frame)):
			sprite.add(anim, i, frame[i], 10)
	sprite.defaultAnimation = df
	return sprite