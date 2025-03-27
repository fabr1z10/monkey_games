import monkey2
from monkey2 import Vec3, Vec4
from . import state
import mupack
import mupack.assets as assets


class VerbHotSpot(monkey2.HotSpot):
    def __init__(self, shape, camera):
        print('dddd')
        super().__init__(shape, 0, camera)
        print('dddd3')

    def onEnter(self):
        self.node.setMultiplyColor(state.COLORS.YELLOW)

    def onLeave(self):
        self.node.setMultiplyColor(state.COLORS.GREEN)

    def onClick(self, pos):
        print('ciao',pos)

def init():
    # rooms =readYAML('assets/rooms.yaml')
    # #print(rooms)
    # #exit(1)
    # assetman.rooms = rooms['rooms']
    # #print(assetman.rooms['castle_west'])
    # #exit(1)
    # assetman.items = rooms['items']
    #
    # assetman.sprites = readYAML('assets/assets.yaml')['sprites']
    # assetman.quads = readYAML('assets/assets.yaml')['quads']
    # #assetman.items = readYAML('assets/rooms.yaml')['items']
    # assetman.strings = readYAML('assets/strings.yaml')['strings']
    mupack.readStrings('assets/strings.yaml')
    mupack.readRooms('assets/rooms.yaml')

def create_room():
    print('room is:', assets.state.room)
    if assets.state.room not in assets.rooms:
        mupack.exit_with_err(f"Don't know room: {assets.state.room}")
    room_info = assets.rooms[assets.state.room]
    tex_list = room_info.get('textures', [0])

    room = monkey2.Room()


    monkey2.game().makeCurrent(room)

    hw = state.WIDTH // 2
    hh = state.HEIGHT // 2
    # create main camera
    viewport = Vec4(0, state.MAIN_VIEW_Y, state.WIDTH, state.MAIN_VIEW_HEIGHT)
    cam = monkey2.CamOrtho(state.WIDTH, state.MAIN_VIEW_HEIGHT,
                           viewport=viewport)
    cam.setPosition(
        Vec3(160, 136//2,  5),
        Vec3(0, 0, -1),
        Vec3(0, 1, 0))

    cam_ui = monkey2.CamOrtho(state.WIDTH, state.HEIGHT,
                              viewport=Vec4(0, 0, state.WIDTH, state.HEIGHT))
    cam_ui.setPosition(
        Vec3(hw, hh, 5),
        Vec3(0, 0, -1),
        Vec3(0, 1, 0))
    room.addCamera(cam)
    room.addCamera(cam_ui)

    ce = monkey2.CollisionEngine(80, 80)
    room.collisionEngine = ce

    monkey2.loadAsset('main', 'petscii.yaml', 0, tex_list)
    monkey2.loadAsset('uimain', 'petscii.yaml', 1, tex_list)
    room.addBatch(monkey2.LineBatch(1000, 0))
    room.addBatch(monkey2.LineBatch(1000, 1))

    root = room.root()

    # add mouse controller
    # add cursor
    cursor = monkey2.Node()
    cursor.setModel(monkey2.getModel('uimain/cursor'))
    root.add(cursor)
    c=monkey2.adventure.MouseController(10)
    #c.setOnClick(scripts.on_left_click)
    #c.setOnRightClick(scripts.on_right_click)
    c.setCursor(cursor)
    c.addSequence(['default'])
    #c.addSequence(['arrow'])
    root.add(c)
    room.hotSpotManager = c

    for key, value in state.VERBS.items():
        t = monkey2.Text('uimain/c64', mupack.eval_string(value['text']), state.COLORS.GREEN)
        shape = monkey2.shapes.Rect(t.size.x, t.size.y, anchor=monkey2.Vec2(0,1))
        hotspot = VerbHotSpot(shape, 1)
        t.addComponent(hotspot)
        #on_click = getattr(ui, value['on_click']) if 'on_click' in value else ui.on_click_verb(key)
        #t.add_component(monkey.components.MouseArea(monkey.shapes.AABB(0, box_size[0], -8, -8+box_size[1]), 0, 1,
            #on_enter=ui.on_enter_verb, on_leave=ui.on_leave_verb, on_click=on_click, batch='line_ui'))
        #t.set_position(value['pos'][0], value['pos'][1], 0)
        t.setPosition(value['pos'])
        snode = monkey2.Node()
        snode.setModel(shape.toModel(monkey2.ModelType.WIRE), 3)
        snode.setMultiplyColor(state.COLORS.GREEN)
        t.add(snode)
        root.add(t)

    #mupack.assets.state.room ='sucal'
    print(room_info)
    for key, source_item in room_info.get('nodes', {}).items():
        print(f' -- creating object: {key} ...')
        node = mupack.nodeBuilder(source_item)
        root.add(node)
        #nodo = builder.nodeBuilder(source_item)
        #gameRoot.add(nodo)

    for key, source_item in assets.items.items():
        ir = source_item.get('room', None)
        if ir == assets.state.room:
            print(f' -- adding dynamic item: {key}')
            root.add(mupack.nodeBuilder(source_item))



    return room
