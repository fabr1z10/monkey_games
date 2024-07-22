import monkey

from . import settings
from . import item_builders
from . import utils


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




    root = room.root()

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
                root.add(utils.makeWalkableCollider(hole['poly']))

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
            root.add(item_builders.build(desc))
            # item_type = desc.get('type')
            # if item_type:
            #     f = globals().get(item_type)
            #     if f:
            #         node = f(desc)
            #         game_node.add(node)
            #         area(node, desc)
            #         game_state.nodes[item] = node.id