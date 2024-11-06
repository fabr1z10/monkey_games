import monkey
from . import values


# bouncing object
class FoeController(monkey.components.Controller2D):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.addCallback(self.ciao)
    self.vy = 0


  def ciao(self, dt):
    self.vy -= 50.0 * dt
    self.move((0, self.vy*dt), False)
    if self.grounded:
      self.vy = abs(self.vy)

class FoeController2(monkey.components.Controller2D):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.addCallback(self.ciao)
    self.addCallback(self.dead)
    self.vy = 0
    self.dir=-1
    self.timer = 0

  def dead(self, dt):
    self.timer += dt
    if self.timer > 2:
      self.node.remove()

  def ciao(self, dt):
    self.vx = self.dir * 20 * dt
    self.vy -= 50.0 * dt
    self.move((self.vx, self.vy*dt), False)
    if self.grounded and self.isFalling(self.dir):
      self.dir = -self.dir
    if self.grounded and self.node.x > 140:
      self.vy = 30


class Goomba(monkey.Node):

  def __del__(self):
    print('HALLLN')
  def pippo(self):
    self.remove()

  def __init__(self, x, y):
    super().__init__()
    #monkey.engine().storeRef(self)
    self.set_position(x, y)
    self.set_model(monkey.models.getSprite('gfx/goomba'), batch='gfx')
    # add collider
    collider = monkey.components.Collider(values.FLAG_FOE, values.FLAG_PLAYER,
		values.TAG_FOE, monkey.shapes.AABB(-8, 8, 0, 16))
    #collider.setResponse(values.TAG_PLAYER, on_enter=self.on_hit_by_player)

    self.add_component(collider)
    self.controller = FoeController2(size=(16,16), speed=20, acceleration=500,
		jump_height=128, time_to_jump_apex=1)
    self.add_component(self.controller)