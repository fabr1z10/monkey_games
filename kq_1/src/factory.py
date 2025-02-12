import monkey2
import yaml
from . import assetman
from . import state
def readYAML(file):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
        return data

def init():
    assetman.sprites = readYAML('assets/assets.yaml')['sprites']
    assetman.rooms = readYAML('assets/rooms.yaml')['rooms']


def create_room():
    room = monkey2.Room()
    # get the current room
    print(f" -- Loading room: {state.room}")
    assert(state.room in assetman.rooms)
    ri = assetman.rooms[state.room]

    # add collision engine
    room.collisionEngine = monkey2.CollisionEngine()
    # create main camera
    viewport = (2, 25, state.ROOM_WIDTH, state.ROOM_HEIGHT)
    cam = monkey2.CamOrtho(state.ROOM_WIDTH, state.ROOM_HEIGHT, viewport=viewport)
    cam.setPosition([state.ROOM_WIDTH // 2,state.ROOM_HEIGHT // 2,5], [0,0,-1], [0,1,0])
    room.addCamera(cam)

    batch = monkey2.QuadBatch(10000, 0, 512, 512, 16)
    #batch.addTexture('kq1.png')

    room.addBatch(batch)

    room.addBatch(monkey2.LineBatch(1000, 0))

    monkey2.game().makeCurrent(room)

    root = room.root()
    #root.add(assetman.makeSpriteNode('bg', 0, 0, 0, batch, z=-1))

    # add player
    player = assetman.makeSpriteNode('graham', 20, 10, 0, batch, dynamicDepth=True)
    root.add(player)

    #root.add(assetman.makeSpriteNode('alligator', 30, 10, 0, batch, dynamicDepth=True))
    #root.add(assetman.makeSpriteNode('tree_castle', 198, 39, 0, batch, dynamicDepth=True))

    walkarea_node = monkey2.Node()
    main_walkarea = None
    i = 0
    for w in ri.get('walkareas', []):
        n = monkey2.adventure.WalkArea(w['poly'], 1, state.WALKAREA_COLORS[i])
        for hole in w.get('holes', []):
            n.addHole(hole)
        if main_walkarea is None:
            main_walkarea = n
        walkarea_node.add(n)
        i += 1
    root.add(walkarea_node)


    scheduler = monkey2.Scheduler()
    root.add(scheduler)
    c=monkey2.adventure.MouseController(0, main_walkarea, player, scheduler, 50)
    root.add(c)


    return room
