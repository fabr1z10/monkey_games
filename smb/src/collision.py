import monkey
import settings
from .items import Mario


class PlayerVsBrick(monkey.CollisionResponse):
    def __init__(self, tag1, tag2):
        super().__init__(tag1, tag2)

    def onStart(self, player, brick, move, who):
        print('START')
        brick.node.parent.hit(player.node)


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

class PlayerVsGoomba(monkey.CollisionResponse):
    def __init__(self, tag1, tag2):
        super().__init__(tag1, tag2)

    def onStart(self, player, goomba, move, who):
        print('figsa')
        if player.node.invincible:
            return
        if who == 0 and move[1] < 0:
            goomba.node.die()
            player.node.bounceOnFoe()
        else:
            if settings.state == 0:
                # dead
                player.node.controller.setState(1)
            else:
                player.node.changeMode(0)


    def onEnd(self, p, f):
        pass


class PlayerVsKoopa(monkey.CollisionResponse):
    def __init__(self, tag1, tag2):
        super().__init__(tag1, tag2)

    def onStart(self, player, koopa, move, who):
        if player.node.invincible:
            return

        if koopa.node.controller.state == 1:
            print(player.node.x, koopa.node.x, koopa.node.dir)
            koopa.node.dir = 1 if player.node.x < koopa.node.x else -1
            print(player.node.x, koopa.node.x, koopa.node.dir)
            koopa.node.controller.setState(2)
        else:
            if who == 0 and move[1] < 0:
                koopa.node.die()
                player.node.bounceOnFoe()
            else:
                if settings.state == 0:
                    # dead
                    player.node.controller.setState(1)
                else:
                    player.node.changeMode(0)


    def onEnd(self, p, f):
        pass