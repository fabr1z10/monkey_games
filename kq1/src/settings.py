import monkey

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
room='test3d'
rooms = {}
items = {}
strings = {}