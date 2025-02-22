import monkey2
import yaml
from . import assetman
from . import state
from . import scripts

class RoomStart:
    def __init__(self):
        self.f = []

    def start(self):
        print('ficanera')
        for g in self.f:
            g()

def readYAML(file):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
        return data

def init():
    assetman.sprites = readYAML('assets/assets.yaml')['sprites']
    assetman.rooms = readYAML('assets/rooms.yaml')['rooms']


def create_room():
    room = monkey2.Room()
    state.IDS = {}
    a = RoomStart()
    room.setStartUpFunction(a.start)
    # create main camera
    viewport = (2, 25, state.ROOM_WIDTH, state.ROOM_HEIGHT)
    cam = monkey2.CamOrtho(state.ROOM_WIDTH, state.ROOM_HEIGHT, viewport=viewport)
    cam.setPosition([state.ROOM_WIDTH // 2,state.ROOM_HEIGHT // 2,5], [0,0,-1], [0,1,0])
    room.addCamera(cam)

    cam2 = monkey2.CamOrtho(320, 200)
    cam2.setPosition([160, 100, 5], [0,0,-1], [0,1,0])
    room.addCamera(cam2)

    room.collisionEngine = monkey2.CollisionEngine()


    # this also creates batch / textures etc.
    monkey2.loadAsset('main', 'assets.yaml', 0)
    monkey2.loadAsset('ui', 'assets.yaml', 1)
    room.addBatch(monkey2.LineBatch(1000, 0))


    root = room.root()
    # m = monkey2.Node()
    # m.setModel(monkey2.getModel('main/alligator'))
    # m.setPosition((128,100,0))
    # root.add(m)
    #
    # player = monkey2.Node()
    # player.setModel(monkey2.getModel('main/graham'))
    # player.setPosition((168,100,0))
    # root.add(player)
    # a = monkey2.Node()
    # a.setModel(monkey2.getModel('main/bg1'))
    # a.setPosition((0,0,-10))
    # root.add(a)
    # a = monkey2.Text('main/sierra', 'Alligator.')
    # a.setPosition((128,50,0))
    # root.add(a)
    # get the current room

    print(f" -- Loading room: {state.room}")
    #assert(state.room in assetman.rooms)
    ri = assetman.rooms[state.room]
    #
    # # add collision engine


    #
    # batch = monkey2.QuadBatch(10000, 0, 512, 512, 16)
    # #batch.addTexture('kq1.png')
    #
    # room.addBatch(batch)
    #
    #
    # monkey2.game().makeCurrent(room)
    #
    # root = room.root()
    # #root.add(assetman.makeSpriteNode('bg', 0, 0, 0, batch, z=-1))
    #
    # add player
    player = monkey2.Node()
    player.setModel(monkey2.getModel('main/graham'))
    player.addComponent(monkey2.DepthScale(166, 0))
    player.setPosition([10,10,0])
    root.add(player)
    #
    # #root.add(assetman.makeSpriteNode('alligator', 30, 10, 0, batch, dynamicDepth=True))
    # #root.add(assetman.makeSpriteNode('tree_castle', 198, 39, 0, batch, dynamicDepth=True))
    walkarea_node = monkey2.Node()
    main_walkarea = None
    #player=None
    i = 0
    for w in ri.get('walkareas', []):
        n = monkey2.adventure.WalkArea(w['poly'], 2, state.WALKAREA_COLORS[i])
        for hole in w.get('holes', []):
            n.addHole(hole)
        for l in w.get('lines', []):
            n.addLine(l)
        if main_walkarea is None:
            main_walkarea = n
        walkarea_node.add(n)
        state.IDS[f'WALKAREA_{i}'] = n.id
        i += 1
    root.add(walkarea_node)

    no = monkey2.Node()

    # #root.add(assetman.makeSpriteNode('prova', 42, 50, 0, batch, dynamicDepth=True, wa=main_walkarea))
    for item in ri.get('nodes', []):
        model = item.get('model')
        pos = item.get('pos', [0,0,0])
        nodo = monkey2.Node()
        nodo.setPosition(pos)
        nodo.setModel(monkey2.getModel(model))
        if item.get('depth'):
            nodo.addComponent(monkey2.DepthScale(166, 0))
        walk = item.get('walk', None)
        if walk:
            if 'poly' in walk:
                shape = monkey2.shapes.Polygon(walk['poly'])
                main_walkarea.addHole(walk['poly'], nodo)
            else:
                shape = monkey2.shapes.Polygon(walk['lines'])
                main_walkarea.addLine(walk['lines'], nodo)
            nodo.addComponent(monkey2.Collider(shape))

        script = item.get('script', None)
        if script:
            a.f.append(getattr(scripts, script)(nodo))

        root.add(nodo)

    # #     z = item[3] if len(item)>3 else None
    # #     root.add(assetman.makeSpriteNode(item[0], item[1], item[2], 0, batch, z=z if z else 0,
    # #                                      dynamicDepth=(z is None), wa=main_walkarea))
    # #

    cursor = monkey2.Node()
    cursor.setModel(monkey2.getModel('ui/cursor'))
    root.add(cursor)
    scheduler = monkey2.Scheduler()
    state.IDS['SCHEDULER'] = scheduler.id
    root.add(scheduler)
    c=monkey2.adventure.MouseController(0, main_walkarea, player, scheduler, 50)
    c.setCursor(cursor, ['walk', 'look'])
    root.add(c)
    room.hotSpotManager = c
    #
    # #a = monkey2.adventure.Obstacle('start.png', 86, 167, 118, 128)

    return room
