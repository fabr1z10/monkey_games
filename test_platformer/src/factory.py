import monkey

from .mario import Mario
from .items import RectangularPlatform
from .foes import Goomba

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
  a = RectangularPlatform(0, 0, 0, 0, 20, 2, tw=2, th=2)
  #a =Mario(32,128)
  root.add(a)#RectangularPlatform(0, 0, 0, 0, 20, 2, tw=2, th=2))
  #root.add(Cane())
  #player = monkey.Node()
  #player.set_position(32, 128)
  #pc = monkey.components.Collider(FLAG_PLAYER, FLAG_FOE, 0, monkey.shapes.AABB(-8, 8, 0, 16))
  #def pippo(foe):
  #  foe.node.remove()


  #pc.setResponse(TAG_FOE, on_enter=pippo)
  #player.add_component(pc)
  #player.add_component(monkey.components.PlayerController2D(size=(16,16), speed=100, acceleration=500,
  #jump_height=128, time_to_jump_apex=1))
  #player.add_component(monkey.components.Follow(0))
  root.add(Mario(32, 128))
  root.add(Goomba(128, 40))




def create_room(room):
  test2(room)