rooms = dict()
items = dict()
strings = dict()
tag_to_id = dict()

def getItem(id: str):
    return items['items'][id]




inventory = {
    'dave': [],
    'bernard': []
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
fridge = 'closed'
loose_panel = 'closed'
faucet = 'closed'
maindoor_unlocked = True

light_reactor = False
light_library = False

baselines = []

def getDoormatSize():
    return [0, 64 if doormat =='open' else 88, 0, 8]