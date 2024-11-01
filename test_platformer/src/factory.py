import monkey
import math

FLAG_PLAYER = 1
FLAG_FOE = 4
FLAG_PLATFORM = 2

# moving platform
def make_moving_platform(p0, delta, time):
  mp = monkey.Node()
  mp.add_component(monkey.components.Collider(FLAG_PLATFORM, FLAG_PLAYER, 1, monkey.shapes.Rect(32, 8)))
  mover = monkey.components.Mover()
  mover.add(monkey.actions.Move(0, p0, 0))
  mover.add(monkey.actions.MoveBy(0, delta, time))
  mp.add_component(mover)
  #mp.set_position(160, 120)
  return mp

class RectangularPlatform(monkey.Node):
  def __init__(self, x, y, width, height, tw=1, th=1):
    super().__init__()
    platform_width = width * tw * 8
    platform_height = height * th * 8
    tp= monkey.TileParser('gfx')
    self.set_model(tp.parse('Q {0},{1},{2},{3},{4},{5}'.format(x,y,tw,th,width,height)))
    self.add_component(monkey.components.Collider(FLAG_PLATFORM, 0, 1, monkey.shapes.AABB(0, platform_width, 0, platform_height)))


class FoeController(monkey.components.CustomController2D):
  def __init__(self, **kwargs):
    super().__init__(self.ciao, **kwargs)
    self.vy = 0

  def ciao(self, dt):
    self.vy -= 50.0 * dt
    self.move((0, self.vy*dt), False)
    if self.grounded:
      print('grounded')
      self.vy = abs(self.vy)






class Foe(monkey.Node):
  def __init__(self):
    super().__init__()
    self.set_position(64,128)
    self.add_component(monkey.components.Collider(FLAG_FOE, 0, 0, monkey.shapes.AABB(-8, 8, 0, 16)))
    self.add_component(FoeController(size=(16,16), speed=100, acceleration=500,
                                                      jump_height=128, time_to_jump_apex=1))




def test1(room):
  world_size = (512, 240)
  cam = monkey.CamOrtho(256, 240,
                        viewport=(0, 0, 256, 240),
                        bounds_x=(128, world_size[0]-128), bounds_y=(120, world_size[1]-120))
  room.add_runner(monkey.CollisionEngine2D(80, 80))
  room.add_camera(cam)
  room.add_batch('lines', monkey.LineBatch(max_elements=200, cam=0))
  root = room.root()

  # adding a platform
  platform1 = monkey.Node()
  platform1.add_component(monkey.components.Collider(FLAG_PLATFORM, 0, 1, monkey.shapes.AABB(0, 320, 0, 32)))
  root.add(platform1)

  platform2 = monkey.Node()
  platform2.add_component(monkey.components.Collider(FLAG_PLATFORM, 0, 1, monkey.shapes.AABB(160, 240, 0, 64)))
  root.add(platform2)

  platform3 = monkey.Node()
  platform3.add_component(monkey.components.Collider(FLAG_PLATFORM, 0, 1, monkey.shapes.AABB(0, 16, 0, 64)))
  root.add(platform3)

  platform4 = monkey.Node()
  platform4.add_component(monkey.components.Collider(FLAG_PLATFORM, 0, 1, monkey.shapes.ConvexPoly([0,0,160,0,160,30])))
  platform4.set_position(320,32)
  root.add(platform4)

  # moving platform
  root.add(make_moving_platform((160, 64), (128, 0), 3.0))
  root.add(make_moving_platform((140, 64), (0, 128), 3.0))


  player = monkey.Node()
  player.set_position(32, 128)
  player.add_component(monkey.components.Collider(FLAG_PLAYER, 0, 0, monkey.shapes.AABB(-8, 8, 0, 16)))
  player.add_component(monkey.components.Controller2D(size=(16,16), speed=100, acceleration=500,
                                                      jump_height=128, time_to_jump_apex=1))
  player.add_component(monkey.components.Follow(0))
  root.add(player)

def test2(room):
  world_size = (512, 240)
  cam = monkey.CamOrtho(256, 240,
                        viewport=(0, 0, 256, 240),
                        bounds_x=(128, world_size[0]-128), bounds_y=(120, world_size[1]-120))
  room.add_runner(monkey.CollisionEngine2D(80, 80))
  room.add_camera(cam)
  room.add_batch('lines', monkey.LineBatch(max_elements=200, cam=0))
  room.add_batch('gfx', monkey.SpriteBatch(max_elements=10000, cam=0, sheet='1'))
  root = room.root()



  #m = monkey.Node()
  #m.set_position(128,128)
  #tp= monkey.TileParser('gfx')
  #m.set_model(tp.parse('Q  0,0,2,2,69,2;'))
  #root.add(m)

  root.add(RectangularPlatform(0, 0, 69, 2, tw=2, th=2))
  #root.add(Cane())
  player = monkey.Node()
  player.set_position(32, 128)
  player.add_component(monkey.components.Collider(FLAG_PLAYER, 0, 0, monkey.shapes.AABB(-8, 8, 0, 16)))
  player.add_component(monkey.components.PlayerController2D(size=(16,16), speed=100, acceleration=500,
                                                      jump_height=128, time_to_jump_apex=1))
  player.add_component(monkey.components.Follow(0))
  root.add(player)
  root.add(Foe())




def create_room(room):
  test2(room)