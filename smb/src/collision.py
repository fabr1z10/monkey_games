import monkey
import settings
from .items import Mario


class PlayerVsBrick(monkey.CollisionResponse):
    def __init__(self, tag1, tag2):
        super().__init__(tag1, tag2)

    def onStart(self, player, brick, move, who):
        print('START')
        brick.node.parent.hit()

    def onEnd(self, p, f):
        print('END COLLISION')

class PlayerVsMushroom(monkey.CollisionResponse):
    def __init__(self, tag1, tag2):
        super().__init__(tag1, tag2)

    def onStart(self, player, mushroom, move, who):
        mushroom.node.remove()
        if settings.state == 0:
            settings.state = 1
            a = Mario(player.node.x, player.node.y)
            player.node.parent.add(a)
            player.node.remove()
        #player.node.set_model(monkey.models.getSprite('tiles/supermario'), batch='tiles')
        #player.node.add_component(monkey.components.SpriteCollider(
        #    settings.Flags.PLAYER, settings.Flags.FOE, settings.Tags.PLAYER, batch='lines'))

    def onEnd(self, p, f):
        print('END COLLISION')