import monkey
import math

def create_room(room):
  world_size = (512, 480)
  cam = monkey.CamOrtho(256, 240,
                        viewport=(0, 0, 256, 240),
                        bounds_x=(128, world_size[0]-128), bounds_y=(120, world_size[1]-120))
  room.add_runner(monkey.CollisionEngine2D(80, 80))
  room.add_camera(cam)
  room.add_batch('lines', monkey.LineBatch(max_elements=200, cam=0))
  root = room.root()


  a= monkey.shapes.Circle(32, (50, 60))
  node = monkey.Node()
  node.add_component(monkey.components.Collider(0, 0, 0, a))
  root.add(node)

  player = monkey.Node()
  player.set_position(100, 128)
  player.add_component(monkey.components.VehicleController(32, 24, 16, 16, (8, 4), 100, 50, 1, math.radians(30)))
  player.add_component(monkey.components.Follow(0))
  root.add(player)
