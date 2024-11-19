import monkey


class PlayerVsBubble(monkey.CollisionResponse):
	def __init__(self, tag1, tag2):
		super().__init__(tag1, tag2)

	def onStart(self, player, foe, move, who):
		# print(player.node.x, who, move)
		print(type(player.node))
		print('ciao',foe.node.controller.state)


		if foe.node.controller.state != 0:
			if who == 0 and monkey.isKeyPressed(265) and not player.node.controller.grounded and move[1] < 0:
				#foe.node.blow_up()
				player.node.bounce()
			else:
				print('qui')
				foe.node.blow_up()
		#	#foe.node.remove()
	    #		foe.node.dead()


		#print('START COLLISION')

	def onEnd(self, p, f):
		print('END COLLISION')