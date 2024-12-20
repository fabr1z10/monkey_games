import monkey
import settings

class Walk(monkey.ControllerState):

    def __init__(self, flipOnEdge: bool, speed: float):
        super().__init__()

        self.flipOnEdge = flipOnEdge
        self.speed = speed

    def init(self, node):
        self.g = self.node.controller.gravity
        self.ctrl = self.node.controller
        self.node.flip_x = True

    def update(self, dt):
        self.node.vy += -self.g * dt
        self.ctrl.move((self.speed, self.node.vy * dt), False)
        if self.ctrl.left:
            self.node.flip_x = False
        elif self.ctrl.right:
            self.node.flip_x = True

        if self.ctrl.grounded:
            if self.flipOnEdge and self.ctrl.isFalling(1):
                self.node.flip_x = not self.node.flip_x
            self.node.vy = 0
class Goomba(monkey.Node):
    def __init__(self, **data):
        super().__init__()
        pos = data['pos']
        z = data.get('z', 1)
        self.set_position(pos[0] * settings.tile_size, pos[1] * settings.tile_size, z)
        pal = data.get('pal', None)
        self.vy=0
        #elf.dir = dir
        #self.flip_x = dir < 0

        # model
        sprite = 'tiles/goomba'
        batch = sprite[:sprite.find('/')]
        self.set_model(monkey.models.getSprite(sprite), batch=batch)
        if pal:
            self.setPalette(pal)
        # add collider
        collider = monkey.components.Collider(settings.Flags.FOE,
                                              settings.Flags.PLAYER, settings.Tags.FOE,
                                              monkey.shapes.AABB(-4, 4, 0, 16))
        self.add_component(collider)
        # add controller
        self.controller = monkey.components.Controller2D(size=(16, 16), speed=20, acceleration=500,
                                                      jump_height=48, time_to_jump_apex=1)
        # add states
        self.controller.addState(Walk(True, 0.5))  # addCallback(update=self.updatePosition)
        #self.controller.addState(Jump())
        #self.controller.addState(JumpHor())
        #self.controller.addState(PrepareJump())
        self.add_component(self.controller)
        self.controller.setState(0)