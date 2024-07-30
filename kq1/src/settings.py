import monkey
from nutree import Tree, Node

def monkeyAssert(cond, msg):
    if not cond:
        print("\033[31;1m" + msg + "\033[0m")
        exit(1)

device_size = (320, 200)
title = 'New game'
shaders = [
    monkey.SHADER_BATCH_QUAD_PALETTE,
    monkey.SHADER_BATCH_LINES
]


tree = None
room='test3d'
rooms = {}
items = {}
strings = {}
player_id = None
game_node_id = None
text_node_id = None
parser_id = None
# half-width and half-height
collider_size = [1, 1]
last_action = None
wman = None


def getItem(id):
    global items
    return items[id]



class CollisionFlags:
    player = 1
    wall = 2
    foe = 4
    hotspot = 8

class CollisionTags:
    player = 0
    foe = 1

class Keys:
    restart = 299
    F3 = 292
    enter = 257
    inventory = 258
    view_item = 293 # F4
    right = 262
    left = 263
    up = 265
    down =264

class Colors:
    White = (1,1,1,1)