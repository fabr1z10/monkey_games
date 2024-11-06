import monkey


class MarioVsGoomba(monkey.CollisionResponse):
	# def __init__(self, tag1, tag2):
	# 	super().__init__(tag1, tag2)

	def onStart(self, player, foe, move, who):
		# print(player.node.x, who, move)
		print(type(player.node))
		print(type(foe.node))


		if who == 0 and move[1] < 0:
			print('removing')
			#foe.node.remove()
			foe.node.setAnimation('dead')
			#print(type(player.node))
			#print(type(foe.node))
			foe.node.controller.setState(1)
			player.node.bounceOnFoe()

		print('START COLLISION')

	def onEnd(self, p, f):
		print('END COLLISION')

# def onEnd(self, mario, goomba):
# 	print('END COLLISION')
