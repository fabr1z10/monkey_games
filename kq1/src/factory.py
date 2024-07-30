import yaml
import monkey
from nutree import Tree, Node
from . import settings
from . import item_builders
from . import utils
from . import data
from . import scripts
from collections import deque
from addict import Dict


def init():
    # load all items
    items = monkey.read_data_file('items.yaml')
    for key, value in items['items'].items():
        value['iid'] = -1
        value['name'] = key
        value['active'] = value.get('active', True)
    settings.items = Dict(items['items'])

    #exit(1)
    #for key, value in items['items'].items():
    #    settings.items[key] = AttrDict(value)
    print(settings.items)
    print(settings.items.rock.moved)
    #exit(1)

    #settings.parser = monkey.read_data_file('parser.yaml')
    settings.tree = Tree("kq1")
    complete = False

    def addToTree(key, value):
        if key in settings.tree:
            return
        parent = value.get('parent', None)
        p = settings.tree.find(parent) if parent is not None else settings.tree
        if p is None:
            if parent not in settings.items:
                print('ERROR: invalid parent',parent)
                exit(1)
            p = addToTree(parent, settings.items[parent])
        n = p.add(key)
        return n

    for key, value in settings.items.items():
        addToTree(key, value)
    settings.tree.print()


    print(' -- loaded', len(settings.items), 'items.')
    strs = monkey.read_data_file('strings.yaml')
    settings.strings = strs['strings']
    settings.parser = strs['parser']

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
    room.add_batch('tri', monkey.TriangleBatch(max_elements=1000, cam=0))
    room.add_batch('tri2', monkey.TriangleBatch(max_elements=1000, cam=1))
    root = room.root()

    game_node = monkey.Node()
    text_node = monkey.Node()


    root.add(utils.makeScoreBar())
    root.add(game_node)
    root.add(text_node)

    kb = monkey.components.Keyboard()
    kb.add(settings.Keys.restart, 1, 0, scripts.restart_room)
    kb.add(settings.Keys.F3, 1, 0, scripts.history)
    #kb.add(settings.Keys.inventory, 1, 0, inventory.show_inventory)
    #kb.add(settings.Keys.view_item, 1, 0, inventory.show_view_item)
    game_node.add_component(kb)

    room_info = settings.getItem(settings.room)

    on_start = room_info.get('on_start')
    if on_start:
        room.addOnStart(getattr(scripts, on_start))

    # add walkarea
    wareas = room_info.get('walkareas')
    assert wareas, 'No walkareas defined.'
    wman = monkey.WalkManager([0, 166])
    i = 0
    for warea in wareas:
        outline = warea['poly']
        area = monkey.WalkArea(outline, 2)
        # holes
        if warea and 'holes' in warea:
            for hole in warea['holes']:
                mode = hole.get('mode', 'all')
                area.addPolyWall(hole['poly'])
                if mode == 'all':
                    game_node.add(utils.makeWalkableCollider(hole['poly']))
        if i == 0:
            data.walkArea = area
            root.add(utils.makeWalkableCollider(outline))
        i+=1
        wman.addWalkArea(area)
    settings.wman = wman
    room.add_runner(wman)

    # add links
    if 'west' in room_info:
        game_node.add(item_builders.west(room_info['west']))
    if 'east' in room_info:
        game_node.add(item_builders.east(room_info['east']))
    if 'north' in room_info:
        game_node.add(item_builders.north(room_info['north']))
    if 'south' in room_info:
        game_node.add(item_builders.south(room_info['south']))





    for item in room_info.get('items', []):
        game_node.add(item_builders.build(item))

    # place dynamic items
    print (' -- adding dynamic items...')
    print(settings.room)
    for item in settings.tree.find(settings.room).children:
        print(' -- adding',item,type(settings.items))
        itemData = getattr(settings.items, item.name)
        node = item_builders.build(itemData)
        game_node.add(node)
        itemData.iid = node.id

            # item_type = desc.get('type')
            # if item_type:
            #     f = globals().get(item_type)
            #     if f:
            #         node = f(desc)
            #         game_node.add(node)
            #         area(node, desc)
            #         game_state.nodes[item] = node.id
    # create parser
    parser = monkey.TextEdit(batch='ui', font='sierra', prompt='>', cursor='_', width=2000,pal=0, on_enter=utils.process_action)
    parser.set_position(0,24,0)
    text_node.add(parser)

    settings.game_node_id = game_node.id
    settings.text_node_id = text_node.id
    settings.parser_id = parser.id