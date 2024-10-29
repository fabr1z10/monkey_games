import monkey

class Node:

	def __init__(self, data):
		self.pos = data.get('pos', [0, 0])
		self.children = dict()
		self.active = True
		self.open = True
		self.sprite = data.get('sprite', None)
		self.quad = data.get('quad', None)
		self.batch = data.get('batch', None)


	def create(self):
		n = monkey.Node()
		if self.batch and self.quad:
			room = monkey.engine().getRoom()
			if not room.hasBatch(self.batch):
				room.add_batch(self.batch, monkey.SpriteBatch(max_elements=10000, cam=0, sheet=batchId))
			a = monkey.models.Quad(self.batch)
			a.add(self.quad)
			n.set_model(a)
		elif self.sprite:
			batchId = self.sprite[:self.sprite.find('/')]
			n.set_model(monkey.models.getSprite(self.sprite), batch=batchId)
		