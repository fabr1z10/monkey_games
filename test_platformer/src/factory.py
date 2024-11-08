import monkey
import yaml
from .mario import Mario
from .items import RectangularPlatform, LinePlatform
from .foes import Goomba
from .room import GameRoom

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

def test2():
  room = GameRoom((256,240), (512, 240), '1')
  root = room.root()
  a = RectangularPlatform(0, 0, 0, 0, 20, 2, tw=2, th=2)
  root.add(a)
  root.add(LinePlatform(32, 64, 32))
  root.add(Mario(32, 128))
  root.add(Goomba(128, 40))
  return room


def test3():
  level_info = monkey.read_data_file('bblevels.yaml')
  level = level_info[3]

  room = GameRoom((320, 200), (320,200), 'bubble')
  root = room.root()
  tp = monkey.TileParser('gfx')

  tile = level['tile']
  a=level['desc']#'[28,1,28*4,0,1,1,0,0,0,18,1,0,0,0,1,1,28*4,0,1,1,0,0,0,18,1,0,0,0,1,1,28*4,0,1,1,0,0,0,18,1,0,0,0,1,1,28*8,0,28,1]
  pal=level['pal']
  rows = 25
  cols = 28
  array = [[0 for _ in range(cols)] for _ in range(rows)]
  i = 0
  row=0
  col=0
  while i < len(a):
    if a[i] == 0 or a[i] == 1:
      array[row][col]=a[i]
      col+=1
      if col>=cols:
        col = 0
        row += 1
      i += 1
    else:
      for j in range(a[i]):
        print (row,col)
        array[row][col] = a[i+1]
        col += 1
        if col>=cols:
          col = 0
          row += 1
      i += 2
  print(array)
  # find horizontal platforms
  i = 0
  j = 0
  level = monkey.Node()
  level.set_position(16, 0)
  while i < rows:
    while j < cols:
      if array[i][j] == 1:
        is_platform = (i < rows-1 and array[i+1][j] == 0)
        value_to_check = 0 if is_platform else 1
        # find length
        istart = j
        while j < cols and array[i][j] == 1 and (i==rows-1 or array[i+1][j] == value_to_check):
          j += 1
        length = j-istart
        print('Found horizontal platform starting at (',i,', ',istart,') with length ', length)
        if is_platform:
          lp = LinePlatform(istart*8, i*8, length, oy=10) if is_platform else monkey.Node()
        else:
          lp = monkey.Node()
          lp.set_position(istart * 8, i * 8)
        model ='Q {0},{1},1,1,{2},1'.format(tile[0], tile[1], length)
        print(model)
        lp.set_model(tp.parse(model))
        level.add(lp)
      else:
        j += 1
    i += 1
    j = 0
  root.add(level)
  # shade effect
  shade_tiles = {
    (0,0,1): (1,2),
    (0,1,0): (2,2),
    (0,1,1): (1,1),
    (1,0,0): (2,1),
    (1,0,1): (0,1),
    (1,1,0): (0,2),
    (1,1,1): (0,1)
  }
  shade_str = 'PAL {0};'.format(pal)

  i=0
  j=0
  while i < rows:
    while j < cols:
      # in order to determine shader, for ij I need to check the 3 neighboring cells
      # i(j-1), (i+1)(j-1), i+1(j), which we call a, b and c
      if array[i][j] == 1:
        j += 1
        continue
      a = 1 if j == 0 else array[i][j-1]
      b = 0 if i == rows- 1 else 1 if j == 0 else array[i+1][j-1]
      c = 0 if i == rows -1 else array[i+1][j]

      if a == 0 and b == 0 and c == 0:
        j += 1
        continue
      tile = shade_tiles[(a,b,c)]
      print('add shade at',j,i)
      shade_str += 'GO {0},{1};Q {2},{3},1,1,1,1;'.format(j,i,tile[0], tile[1])
      j += 1
    i +=1
    j = 0
  shadeNode = monkey.Node()
  shade_str += 'PAL 0;'
  #print(shade_str)
  shadeNode.set_model(tp.parse(shade_str))
  level.add(shadeNode)
  root.add(Mario(32, 128, 'gfx/bub', 6, 16, slide='walk',
                 jumpUp='jump_up'))







  return room


  node = monkey.Node()
  node.set_model(tp.parse('Q 0,0,1,1,2,25;GO 2,0;Q 0,0,1,1,25,1;GO 27,0;Q 0,0,1,1,2,25;'
                          'GO 2,24;Q 0,0,1,1,25,1'))
  root.add(node)
  return room





def create_room():
  return test3()
  #r = GameRoom((512, 240))
  #return r
