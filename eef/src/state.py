import monkey2




WIDTH = 320
HEIGHT = 200
MAIN_VIEW_HEIGHT = 136
MAIN_VIEW_Y = 56

DEFAULT_VERB = 'walkto'

VERBS = {
    'push': {
        'text': 0,
        'pos': monkey2.Vec3(2, 47, 0)
    },
    'pull': {
        'text': 1,
        'pos': monkey2.Vec3(2, 39, 0)
    },
    'give': {
        'text': 2,
        'pos': monkey2.Vec3(2, 31, 0),
        'objects': 2,
        'preposition': 15
    },
    'open': {
        'text': 3,
        'pos': monkey2.Vec3(66, 47, 0)
    },
    'close': {
        'text': 4,
        'pos': monkey2.Vec3(66, 39, 0)
    },
    'read': {
        'text': 5,
        'pos': monkey2.Vec3(66, 31, 0)
    },
    'walkto': {
        'text': 6,
        'pos': monkey2.Vec3(122, 47, 0)
    },
    'pickup': {
        'text': 7,
        'pos': monkey2.Vec3(122, 39, 0)
    },
    'whatis': {
        'text': 8,
        'pos': monkey2.Vec3(122, 31, 0)
    },
    'newkid': {
        'text': 9,
        'pos': monkey2.Vec3(194, 47, 0)
        #'on_click': 'newkid'
    },
    'unlock': {
        'text': 10,
        'pos': monkey2.Vec3(194, 39, 0)
    },
    'use': {
        'text': 11,
        'pos': monkey2.Vec3(194, 31, 0)
    #     'objects': 2,
    #     'preposition': 30
    },
    'turnon': {
        'text': 12,
        'pos': monkey2.Vec3(258,47, 0)
    },
    'turnoff': {
        'text': 13,
        'pos': monkey2.Vec3(258, 39, 0)
    },
    'fix': {
        'text': 14,
        'pos': monkey2.Vec3(258, 31, 0)
    }
}

class COLORS:
    WHITE = monkey2.Color("#ffffff")
    GREEN = monkey2.Color("#62d532")
    YELLOW = monkey2.Color("#ffff46")
    PURPLE = monkey2.Color("#aa40f5")
