import monkey2
from monkey2 import Vec3, Vec4, Node
from . import state
import mupack
import mupack.assets as assets
from . import scripts

# class VerbHotSpot(monkey2.HotSpot):
#     def __init__(self, shape, camera, key):
#         self.key = key
#         super().__init__(shape, 0, camera)
#
#     def onEnter(self):
#         self.node.setMultiplyColor(state.COLORS.YELLOW)
#
#     def onLeave(self):
#         self.node.setMultiplyColor(state.COLORS.GREEN)
#
#     def onClick(self, pos):
#         mupack.assets.state.action = self.key
#         mupack.get_tag('LABEL_ACTION').updateText(mupack.eval_string(state.VERBS[self.key]['text']))

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
    mupack.addScripts(scripts)

# def create_UI(root):
#     for key, value in state.VERBS.items():
#         t = monkey2.Text('uimain/c64', mupack.eval_string(value['text']), state.COLORS.GREEN)
#         shape = monkey2.shapes.Rect(t.size.x, t.size.y, anchor=monkey2.Vec2(0,1))
#         hotspot = VerbHotSpot(shape, 1, key)
#         t.addComponent(hotspot)
#         #on_click = getattr(ui, value['on_click']) if 'on_click' in value else ui.on_click_verb(key)
#         #t.add_component(monkey.components.MouseArea(monkey.shapes.AABB(0, box_size[0], -8, -8+box_size[1]), 0, 1,
#             #on_enter=ui.on_enter_verb, on_leave=ui.on_leave_verb, on_click=on_click, batch='line_ui'))
#         #t.set_position(value['pos'][0], value['pos'][1], 0)
#         t.setPosition(value['pos'])
#         snode = monkey2.Node()
#         snode.setModel(shape.toModel(monkey2.ModelType.WIRE), 3)
#         snode.setMultiplyColor(state.COLORS.GREEN)
#         t.add(snode)
#         root.add(t)
#     # create action label
#     al = monkey2.Text('uimain/c64', mupack.eval_string(state.VERBS[state.DEFAULT_VERB]['text']),
#         state.COLORS.PURPLE)
#     al.setPosition(Vec3(2, 55, 0))
#     mupack.add_tag('LABEL_ACTION', al)
#     root.add(al)
def restart():
	monkey2.closeRoom()


def create_room():
    print('room is:', assets.state.room)
    if assets.state.room not in assets.rooms:
        mupack.exit_with_err(f"Don't know room: {assets.state.room}")
    room_info = assets.rooms[assets.state.room]
    size = room_info['size']
    tex_list = room_info.get('textures', [0])

    room = monkey2.Room()
    monkey2.game().makeCurrent(room)

    hw = state.WIDTH // 2
    hh = state.HEIGHT // 2
    mhh = state.MAIN_VIEW_HEIGHT // 2
    # create main camera
    viewport = Vec4(0, state.MAIN_VIEW_Y, state.WIDTH, state.MAIN_VIEW_HEIGHT)
    cam = monkey2.CamOrtho(state.WIDTH, state.MAIN_VIEW_HEIGHT,
                           viewport=viewport)
    cam.setBounds(hw, size[0] - hw, mhh, mhh, -10., 10.)
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
    lb0 = monkey2.LineBatch(1000, 0)
    lb1 = monkey2.LineBatch(1000, 1)
    room.addBatch(lb0)
    room.addBatch(lb1)


    root = room.root()

    kb = monkey2.Keyboard()
    kb.add(state.KEY_RESTART_ROOM, 1, 0, restart)
    root.addComponent(kb)

    #state.IDS['ROOT'] = root.id


    game_root = Node()
    ui_root = Node()
    mupack.add_tag('UI_ROOT', ui_root)

    root.add(game_root)
    root.add(ui_root)

    # add mouse controller
    cursor = monkey2.Node()
    cursor.setModel(monkey2.getModel('uimain/cursor'))
    root.add(cursor)
    c = monkey2.adventure.MouseController(10)
    c.setOnClick(scripts.on_left_click)
    # # #c.setOnRightClick(scripts.on_right_click)
    c.setCursor(cursor)
    c.addSequence(['default'])
    # #c.addSequence(['arrow'])
    root.add(c)
    room.hotSpotManager = c


    mupack.lucas.create_UI(ui_root, 0, lb1.id)

    walkarea_node = monkey2.Node()
    i = 0
    for w in room_info.get('walkareas', []):
        n = monkey2.adventure.WalkArea(w['poly'], lb0.id, state.COLORS.WHITE)
    #     for hole in w.get('holes', []):
    #         n.addHole(hole)
    #     for l in w.get('lines', []):
    #         n.addLine(l)
    #     #if main_walkarea is None:
        walkarea_node.add(n)
        mupack.add_tag(f'WALKAREA_{i}', n)
    #
    #     i += 1
    #shape= monkey2.shapes.Polygon([10,10,50,10,70,30])
    #walkarea_node.setModel(shape.toModel(monkey2.ModelType.WIRE), lb0.id)
    game_root.add(walkarea_node)
    mupack.add_tag(f'WALKAREA_ROOT', walkarea_node)



    for key, source_item in room_info.get('nodes', {}).items():
        print(f' -- creating object: {key} ...')
        node = mupack.nodeBuilder(key, source_item, lb0.id)
        game_root.add(node)


    for key, source_item in assets.items.items():
        ir = source_item.get('room', None)
        if ir == assets.state.room:
            print(f' -- adding dynamic item: {key}')
            node = mupack.nodeBuilder(key, source_item, lb0.id)
            if node:
                if key == mupack.assets.state.player:
                    mupack.add_tag('PLAYER', node)
                    node.addComponent(monkey2.Follow(0))
                    #mupack.assets.state.ID_PLAYER = 1
                    print(' -- this is player.')
                mupack.add_tag(key, node)
                game_root.add(node)

    scheduler = monkey2.Scheduler()
    mupack.add_tag('SCHEDULER', scheduler)
    root.add(scheduler)

    #print(mupack.assets.ids)
    #print('cursor:',cursor.id)
    #print('cursor:', game_root.id)
    #print('cursor:', walkarea_node.id)
    return room
