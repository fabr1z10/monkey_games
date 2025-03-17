import monkey2
from monkey2 import Vec2, Vec3, Vec4
import yaml
import colorama
from . import assetman
from . import state
from . import scripts
from . import code
from .util import readYAML, exit_with_err
#from .scripts import exit_with_err
from .object_hotspot import ObjectHotSpot



class RoomStart:
    def __init__(self):
        self.f = []

    def start(self):
        for g in self.f:
            g()



def init():
    rooms =readYAML('assets/rooms.yaml')
    #print(rooms)
    #exit(1)
    assetman.rooms = rooms['rooms']
    #print(assetman.rooms['castle_west'])
    #exit(1)
    #assetman.items = rooms['items']

    assetman.sprites = readYAML('assets/assets.yaml')['sprites']
    assetman.quads = readYAML('assets/assets.yaml')['quads']
    #assetman.items = readYAML('assets/rooms.yaml')['items']
    assetman.strings = readYAML('assets/strings.yaml')['strings']


def create_room():
    print(f" -- Loading room: {state.room}")
    if state.room not in assetman.rooms:
        exit_with_err(f"Don't know room: {state.room}")

    ri = assetman.rooms[state.room]
    tex_list = [0]
    tex_list.extend(ri['textures'])
    room = monkey2.Room()
    monkey2.game().makeCurrent(room)

    state.IDS = {}
    startUp = RoomStart()
    room.setStartUpFunction(startUp.start)

    # create main camera
    viewport = Vec4(2, 25, state.ROOM_WIDTH, state.ROOM_HEIGHT)
    cam = monkey2.CamOrtho(state.ROOM_WIDTH, state.ROOM_HEIGHT, viewport=viewport)
    cam.setPosition(
        Vec3(state.ROOM_WIDTH // 2,state.ROOM_HEIGHT // 2, 5),
        Vec3(0, 0, -1),
        Vec3(0, 1, 0))
    room.addCamera(cam)

    # create ui cam
    cam2 = monkey2.CamOrtho(320, 200)
    cam2.setPosition(
        Vec3(160, 100, 5),
        Vec3(0, 0, -1),
        Vec3(0, 1, 0))
    room.addCamera(cam2)

    ce = monkey2.CollisionEngine(80, 80)
    ce.addResponse('player', 'drown', code.drown)
    ce.addResponse('player', 'goto', code.gotoRoom)
    room.collisionEngine = ce

    # # this also creates batch / textures etc.
    # when you load an asset bank -> it has associated a camera
    monkey2.loadAsset('main', 'assets.yaml', 0, tex_list)
    monkey2.loadAsset('ui', 'assets.yaml', 1, tex_list)
    room.addBatch(monkey2.LineBatch(1000, 0))
    room.addBatch(monkey2.TriangleBatch(1000, 0))
    room.addBatch(monkey2.LineBatch(1000, 1))
    room.addBatch(monkey2.TriangleBatch(1000, 1))

    line_batch = 2

    root = room.root()
    kb = monkey2.Keyboard()
    kb.add(state.KEY_RESTART_ROOM, 1, 0, scripts.restart)
    kb.add(state.KEY_INVENTORY, 1, 0, scripts.enter_inventory)
    kb.add(state.KEY_ESC, 1, 0, scripts.exit_inventory)
    root.addComponent(kb)
    state.IDS['ROOT'] = root.id


    gameRoot = monkey2.Node()
    uiRoot = monkey2.Node()
    state.IDS['GAME_ROOT'] = gameRoot.id
    state.IDS['UI_ROOT'] = uiRoot.id
    root.add(gameRoot)
    root.add(uiRoot)

    # a = monkey2.Node()
    # tree = monkey2.shapes.fromImage('main', 1, [86, 167, 118, 127], 10)
    # a.setModel(tree.toModel((1,1,1,1)), line_batch)
    # root.add(a)


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


    print(ri)
    #
    # # add collision engine


    #
    #

    #
    # root = room.root()
    # #root.add(assetman.makeSpriteNode('bg', 0, 0, 0, batch, z=-1))
    #
    # add player

    player = monkey2.Node()
    player.setModel(monkey2.getModel('main/graham'))
    player.addComponent(monkey2.DepthScale(166, 0, state.FLAG_WALK_BLOCK))
    player.setPosition(state.PLAYER_POS)
    player.addComponent(monkey2.Collider(monkey2.shapes.Point(), 1, 2, 'player'))
    pn = monkey2.Node()
    pn.setModel(monkey2.shapes.Point().toModel(monkey2.ModelType.WIRE), 2)
    player.add(pn)
    dir = 'e' if state.PLAYER_DIR == 'w' else state.PLAYER_DIR
    player.animation = f"idle-{dir}"
    player.flipX(state.PLAYER_DIR == 'w')
    gameRoot.add(player)
    state.IDS['PLAYER'] = player.id
    print(' -- player id:',player.id)
    #
    # #root.add(assetman.makeSpriteNode('alligator', 30, 10, 0, batch, dynamicDepth=True))
    # #root.add(assetman.makeSpriteNode('tree_castle', 198, 39, 0, batch, dynamicDepth=True))
    walkarea_node = monkey2.Node()
    main_walkarea = None
    #player=None
    i = 0
    for w in ri.get('walkareas', []):
        n = monkey2.adventure.WalkArea(w['poly'], line_batch, state.COLORS.WALKAREA)
        for hole in w.get('holes', []):
            n.addHole(hole)
        for l in w.get('lines', []):
            n.addLine(l)
        if main_walkarea is None:
            main_walkarea = n
        walkarea_node.add(n)
        state.IDS[f'WALKAREA_{i}'] = n.id
        i += 1
    gameRoot.add(walkarea_node)
    print( ' -- walkarea:',walkarea_node.id)
    # #root.add(assetman.makeSpriteNode('prova', 42, 50, 0, batch, dynamicDepth=True, wa=main_walkarea))
    # add room nodes

    #pnodes = [scripts.eval_field(item, env={'item':item}) for item in ri.get('nodes', [])]
    print('FANUC:',ri.get('nodes', {}))
    for key, source_item in ri.get('nodes', {}).items():
        print(f' -- creating object: {key} ...', end='')
        item = scripts.eval_field(source_item, env={'item': source_item, 'state': state})
        active = item.get('active', True)
        if not active:
            print('NOT ACTIVE')
            continue
        pos = Vec3(item.get('pos', [0,0,0]))
        model = item.get('model')
        nodo = monkey2.Node()
        nodo.setPosition(pos)
        if model:
            nodo.setModel(monkey2.getModel(model))
        anim = item.get('anim', None)
        if anim:
            nodo.animation = anim
        if item.get('depth'):
            nodo.addComponent(monkey2.DepthScale(166, 0, state.FLAG_WALK_BLOCK))
        walk = item.get('walk', None)
        if walk:
            if 'poly' in walk:
                shape = monkey2.shapes.Polygon(walk['poly'])
                main_walkarea.addHole(walk['poly'], nodo)
            else:
                shape = monkey2.shapes.Polygon(walk['lines'])
                main_walkarea.addLine(walk['lines'], nodo)
            nodo.addComponent(monkey2.Collider(shape, state.FLAG_WALK_BLOCK, 0, 'block'))
        collider = item.get('collider', None)
        if collider:
            cl = item['collider']
            flag = cl['flag']
            mask = cl['mask']
            tag = cl['tag']
            shape = monkey2.shapes.Polygon(cl['poly'])
            nodo.addComponent(monkey2.Collider(shape, flag, mask, tag))
            sm = shape.toModel(monkey2.ModelType.WIRE)
            ab = monkey2.Node()
            ab.setModel(sm, line_batch)
            nodo.add(ab)
        if 'hotspot' in item:
            a = monkey2.Node()
            # shape can be automatically generated or can be a rect
            if 'rect' in item['hotspot']:
                rect = item['hotspot']['rect']
                anchor = Vec2() if len(rect) == 2 else Vec2(rect[2], rect[3])
                shape = monkey2.shapes.Rect(rect[0], rect[1], anchor=anchor)
            elif 'poly' in item['hotspot']:
                shape = monkey2.shapes.Polygon(item['hotspot']['poly'])
            else:
                mm = model.split('/')
                qq = assetman.quads[mm[1]]
                shape = monkey2.shapes.fromImage(mm[0], qq['tex'], Vec4(qq['data']), 10)
            a.setModel(shape.toModel(monkey2.ModelType.WIRE), line_batch)
            a.setMultiplyColor(state.COLORS.HOTSPOT)
            hotspot = ObjectHotSpot(source_item, shape, item['hotspot'].get('priority', 0), 0)# monkey2.HotSpot(shape, 0, 0)
            nodo.addComponent(hotspot)
            nodo.userData = item['hotspot']
            nodo.add(a)
        if 'user_data' in item:
            #print('USER=DATA=',item['user_data'])
            if nodo.userData:
                nodo.userData.update(item['user_data'])
            else:
                nodo.userData = item['user_data']
            #print('FUCK',nodo.userData)
        if 'npc' in item:
            npc = item['npc']
            walkAreaId = npc['walkarea']
            walkArea = state.getNode(f"WALKAREA_{walkAreaId}")
            refresh = npc['refresh']
            onRefresh = getattr(code, npc['onRefresh'])
            onReach = getattr(code, npc['onReach'])
            nodo.addComponent(monkey2.NPC(walkArea, refresh, onRefresh, onReach))


        script = item.get('script', None)
        if script:
            fu = getattr(code, script, None)
            if not fu:
                exit_with_err(f"Cannot find script: {script}")
            startUp.f.append(fu(nodo))
        print('OK')
        gameRoot.add(nodo)

    # #     z = item[3] if len(item)>3 else None
    # #     root.add(assetman.makeSpriteNode(item[0], item[1], item[2], 0, batch, z=z if z else 0,
    # #                                      dynamicDepth=(z is None), wa=main_walkarea))
    # #
    print('---processed nodes.')
    # add cursor
    cursor = monkey2.Node()
    cursor.setModel(monkey2.getModel('ui/cursor'))
    root.add(cursor)
    print('cursor',cursor.id)
    # add scheduler
    scheduler = monkey2.Scheduler()
    state.IDS['SCHEDULER'] = scheduler.id
    gameRoot.add(scheduler)

    # scheduler2 = monkey2.Scheduler()
    # state.IDS['SCHEDULER2'] = scheduler2.id
    # root.add(scheduler2)

    # add mouse controller
    c=monkey2.adventure.MouseController(state.Z_CURSOR)
    #c.setOnEnter(scripts.on_enter_hotspot)
    #c.setOnLeave(scripts.on_leave_hotspot)
    c.setOnClick(scripts.on_left_click)
    c.setOnRightClick(scripts.on_right_click)

    c.setCursor(cursor)
    c.addSequence(['walk', 'look', 'use', 'talk', ''])
    c.addSequence(['arrow'])
    gameRoot.add(c)
    state.IDS['MOUSE_CTRL'] = c.id
    room.hotSpotManager = c
    #
    # #a = monkey2.adventure.Obstacle('start.png', 86, 167, 118, 128)
    print('ORA')
    #monkey2.shapes.fromImage('main', 1, [86, 167, 118, 127], 10)
    return room
