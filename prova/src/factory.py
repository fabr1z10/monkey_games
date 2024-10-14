import monkey

def create_room(room):
  size = (448, 30)
  tileSize = 8
  pxw = size[0] * tileSize
  pxh = size[1] * tileSize
  cam = monkey.CamOrtho(256, 240,
                        viewport=(0, 0, 256, 240),
                        bounds_x=(128, pxw-128), bounds_y=(120, 120))
  room.add_camera(cam)
  room.add_batch('lines', monkey.LineBatch(max_elements=200, cam=0))
  room.add_batch('tiles', monkey.SpriteBatch(max_elements=10000, cam=0, sheet='1'))

  root = room.root()

  n = monkey.TileWorld(8, 448, 32, "ciao", "tiles", gfx='data.bin')
  roomData = ""
  a = monkey.Node()

  #a.set_model(monkey.models.from_shape('lines', monkey.shapes.AABB(0,16,0,16), [1,1,1,1], monkey.FillType.Outline))
  a.set_position(32, 96, 0)
  a.add_component(monkey.components.TileController(500, 16, 16, batch='lines'))
  a.add_component(monkey.components.Follow(0))
  root.add(n)
  root.add(a)