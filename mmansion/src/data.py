rooms = dict()
items = dict()
strings = dict()
tag_to_id = dict()

def getItem(id: str):
    return items['items'][id]


def isActive(item):
    return items['items'][item].get('active', True)



inventory = {
    'dave': [],
    'bernard': ['cassette_tape', 'record']
}

delayed_funcs = {
    'dave': None,
    'bernard': None
}


doormat = 'closed'
door_main = 'closed'
door_kitchen = 'closed'
door_dining = 'closed'
door_pantry = 'closed'
door_reactor='closed'
door_living='closed'
door_library='closed'
door_artroom='closed'
door_musicroom='closed'
door_hallway_mid='closed'
door_radio='closed'
door_fitness='closed'

cassette_recorder = 'off'
victrola='empty'
tape_in_recorder = False
rec_start_time = None
vic_start_time = None
time_to_break_vase = 2
vase_break_event = None
chandelier_break_event = None
tape_recorded = 0
music_vase = 'default'
cabinet = 'closed'
cassette_player = 'off'
broken_chandelier=False
hatch='open'
fridge = 'closed'
loose_panel = 'closed'
faucet = 'closed'
maindoor_unlocked = True
pass_green_tentacle = 0
food_given_to_gt = False
drink_given_to_gt = True
light_reactor = False
light_library = False

baselines = []

def getDoormatSize():
    return [0, 64 if doormat =='open' else 88, 0, 8]