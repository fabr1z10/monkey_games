import monkey2


WIDTH = 320
HEIGHT = 200
MAIN_VIEW_HEIGHT = 136
MAIN_VIEW_Y = 54

VERBS = {
    'push': {
        'text': 0,
        'pos': monkey2.Vec3(2, 48, 0)
    },
    'pull': {
        'text': 1,
        'pos': monkey2.Vec3(2, 40, 0)
    },
    'give': {
        'text': 2,
        'pos': monkey2.Vec3(2, 32, 0),
        'objects': 2,
        'preposition': 15
    },
    # 'open': {
    #     'text': 3,
    #     'pos': [65, 45]
    # },
    # 'close': {
    #     'text': 4,
    #     'pos': [65, 37]
    # },
    # 'read': {
    #     'text': 5,
    #     'pos': [65, 29]
    # },
    # 'walkto': {
    #     'text': 6,
    #     'pos': [121, 45]
    # },
    # 'pickup': {
    #     'text': 7,
    #     'pos': [121, 37]
    # },
    # 'whatis': {
    #     'text': 8,
    #     'pos': [121, 29]
    # },
    # 'newkid': {
    #     'text': 9,
    #     'pos': [193, 45],
    #     'on_click': 'newkid'
    # },
    # 'unlock': {
    #     'text': 10,
    #     'pos': [193, 37]
    # },
    # 'use': {
    #     'text': 11,
    #     'pos': [193, 29],
    #     'objects': 2,
    #     'preposition': 30
    # },
    # 'turnon': {
    #     'text': 12,
    #     'pos': [257, 45]
    # },
    # 'turnoff': {
    #     'text': 13,
    #     'pos': [257, 37]
    # },
    # 'fix': {
    #     'text': 14,
    #     'pos': [257, 29]
    # },
}

class COLORS:
    GREEN = monkey2.Color("#62d532")
    YELLOW = monkey2.Color("#ffff46")
    PURPLE = monkey2.Color("#aa40f5")
