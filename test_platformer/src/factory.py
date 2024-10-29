import monkey
import math

def create_room(room):
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
  platform1.add_component(monkey.components.Collider(2, 0, 1, monkey.shapes.AABB(0, 400, 0, 32)))
  root.add(platform1)

  platform2 = monkey.Node()
  platform2.add_component(monkey.components.Collider(2, 0, 1, monkey.shapes.AABB(160, 240, 0, 64)))
  root.add(platform2)

  platform3 = monkey.Node()
  platform3.add_component(monkey.components.Collider(2, 0, 1, monkey.shapes.AABB(0, 16, 0, 64)))
  root.add(platform3)

  platform4 = monkey.Node()
  platform4.add_component(monkey.components.Collider(2, 0, 1, monkey.shapes.ConvexPoly([0,0,160,0,160,30])))
  platform4.set_position(360,32)
  root.add(platform4)


  player = monkey.Node()
  player.set_position(100, 128)
  player.add_component(monkey.components.Controller2D(size=(16,16), gravity=30, speed=100, acceleration=500))
  player.add_component(monkey.components.Follow(0))
  root.add(player)
