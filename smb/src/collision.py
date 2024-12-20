import monkey

class PlayerVsBrick(monkey.CollisionResponse):
    def __init__(self, tag1, tag2):
        super().__init__(tag1, tag2)

    def onStart(self, player, brick, move, who):
        print('START')
        brick.node.parent.hit()

    def onEnd(self, p, f):
        print('END COLLISION')