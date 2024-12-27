import untitled3

class Bar(untitled3.Foo):

	def __init__(self):
		super().__init__()

	def start(self, **kwargs):
		print(kwargs.get('pippo'))
		print('ici')

	def update(self, dt):
		print('here')


c = untitled3.Caller()
c.add(Bar())
c.add(Bar())
c.start(1)

