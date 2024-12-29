import monkey

device_size = (256, 224)
title = 'New game'
shaders = [
    monkey.SHADER_BATCH_QUAD_PALETTE,
    monkey.SHADER_BATCH_LINES
]
DRAW_COLLIDER_OUTLINE='lines'
room = '1-1'
start_position = 0
worlds = dict()
strings = dict()
score = 1500
coins = 1
tile_size = 16
jumpHeight = 72
timeToJumpApex = 0.5
id_main_node = None
id_label_score = None
id_label_coins = None
MarioSpeed = 300
hotspot= None

state = 0
mario_states = [
    {
        'model': 'tiles/mario',
        'height': 16,
        'size': [10, 10, 0],
        'center': [5, 0, 0]
    },
    {
        'model': 'tiles/supermario',
        'size': [10, 30, 0],
        'height': 30,
        'center': [5, 0, 0]
    }
]

class Keys:
    restart = 299


class Flags:
    PLAYER = 1
    FOE = 4

class Tags:
    PLAYER = 0
    FOE = 1
    BRICK_SENSOR = 2
    MUSHROOM = 3
    MUSHROOM_1UP = 4
    GOOMBA = 5
    KOOPA =6
    HOTSPOT=7
    COIN = 8
    HOTSPOT_HOR = 9