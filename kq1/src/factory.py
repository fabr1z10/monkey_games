import monkey

from . import settings
from . import item_builders
from . import utils
from . import data
from . import scripts

def init():
    settings.rooms = monkey.read_data_file('rooms.yaml')
    print (' -- loaded',len(settings.rooms), 'rooms.')
    settings.items = monkey.read_data_file('items.yaml')
    print(' -- loaded', len(settings.items), 'items.')
    settings.strings = monkey.read_data_file('strings.yaml')
    print(' -- loaded', len(settings.strings), 'strings.')

def create_item(data):
    print(data)



def create_room(room):
    ce = monkey.CollisionEngine2D(80, 80)
    room.add_runner(ce)
    room.add_runner(monkey.Scheduler())
    room.add_runner(monkey.Clock())

    viewport = (2, 25, 316, 166)
    cam = monkey.CamOrtho(316, 166,
                          viewport=viewport,
                          bounds_x=(158, 158), bounds_y=(83, 83))
    room.add_camera(cam)
    room.add_batch('lines', monkey.LineBatch(max_elements=200, cam=0))
    ui_cam = monkey.CamOrtho(320,200, viewport=(0,0,320,200), bounds_x=(160,160), bounds_y=(100,100))
    room.add_camera(ui_cam)
    room.add_batch('sprites', monkey.SpriteBatch(max_elements=10000, cam=0, sheet='sprites'))
    room.add_batch('ui', monkey.SpriteBatch(max_elements=10000, cam=1, sheet='sprites'))
    room.add_batch('tri2', monkey.TriangleBatch(max_elements=1000, cam=1))
    root = room.root()

    game_node = monkey.Node()
    text_node = monkey.Node()


    root.add(utils.makeScoreBar())
    root.add(game_node)
    root.add(text_node)

    kb = monkey.components.Keyboard()
    kb.add(settings.Keys.restart, 1, 0, scripts.restart_room)
    #kb.add(settings.Keys.inventory, 1, 0, inventory.show_inventory)
    #kb.add(settings.Keys.view_item, 1, 0, inventory.show_view_item)
    game_node.add_component(kb)

    room_info = settings.rooms[settings.room]

    # add walkarea
    warea = room_info.get('walkarea')
    wman = monkey.WalkManager([0, 166])
    outline = warea['poly'] if warea else [1, 1, 315, 1, 315, 165, 1, 165]
    area = monkey.WalkArea(outline, 2)
    # holes
    if warea and 'holes' in warea:
        for hole in warea['holes']:
            mode = hole.get('mode', 'all')
            area.addPolyWall(hole['poly'])
            if mode == 'all':
                game_node.add(utils.makeWalkableCollider(hole['poly']))
    data.walkArea = area
    wman.addWalkArea(area)
    # also need to add a collider
    room.add_runner(wman)
    root.add(utils.makeWalkableCollider(outline))


    for item in room_info.get('items', []):
        root.add(item_builders.build(item))

    # place dynamic items
    print (' -- adding dynamic items...')
    for item, desc in settings.items.items():
        room = desc.get('room', None)
        if room == settings.room:
            print(' -- adding',item)
            game_node.add(item_builders.build(desc))
            # item_type = desc.get('type')
            # if item_type:
            #     f = globals().get(item_type)
            #     if f:
            #         node = f(desc)
            #         game_node.add(node)
            #         area(node, desc)
            #         game_state.nodes[item] = node.id

    # create parser
    parser = monkey.TextEdit(batch='ui', font='sierra', prompt='>', cursor='_', width=2000,pal=0)#, on_enter=engine.process_action)
    parser.set_position(0,24,0)
    text_node.add(parser)