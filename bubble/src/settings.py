import monkey

device_size = (320, 200)
title = 'Bubble Bobble C64'
shaders = [
    monkey.SHADER_BATCH_QUAD_PALETTE,
    monkey.SHADER_BATCH_LINES
]

TILESIZE = 8
FLAG_PLAYER = 1
FLAG_FOE = 4
FLAG_PLATFORM = 2
FLAG_BUBBLE = 8
FLAG_PLATFORM_SEMI = 32
TAG_PLAYER = 0
TAG_FOE =1
TAG_BUBBLE = 2
BUBBLE_SHOOT_SPEED = 200
BUBBLE_DRIFT_SPEED = 30
DRAW_COLLIDER_OUTLINE = 'lines'

id_player = None
level_data = {}
jmp = {}
level = 1
bubble_path = None

