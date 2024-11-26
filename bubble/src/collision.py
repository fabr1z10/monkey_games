import monkey


class PlayerVsBubble(monkey.CollisionResponse):
	def __init__(self, tag1, tag2):
		super().__init__(tag1, tag2)

	def onStart(self, player, foe, move, who):
		# print(player.node.x, who, move)
		print(type(player.node))
		print('ciao',foe.node.controller.state)
		if foe.node.controller.state == 1:
			if who == 0 and monkey.isKeyPressed(265) and not player.node.controller.grounded and move[1] < 0:
				#foe.node.blow_up()
				player.node.bounce()
			else:
				print('qui')
				foe.node.burstByPlayer()

	def onEnd(self, p, f):
		print('END COLLISION')


class BubbleVsFoe(monkey.CollisionResponse):
	def __init__(self, tag1, tag2):
		super().__init__(tag1, tag2)

	def onStart(self, bubble, foe, move, who):
		if bubble.node.controller.state == 0:
			# create foe bubble
			foe.node.create_bubble()
			foe.node.remove()
			bubble.node.remove()
