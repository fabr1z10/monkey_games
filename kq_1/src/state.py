import monkey2


IDS = {}

def getNode(s: str):
	return monkey2.getNode(IDS[s])

scheduler = None

action = None
target_object = None

def getNode(s: str):
	return monkey2.getNode(IDS[s])

Z_CURSOR = 11
Z_TEXT = 10

KEY_RESTART_ROOM = 299
KEY_INVENTORY = 293
KEY_ESC = 256


TEXT_MARGIN_X = 10
TEXT_MARGIN_Y = 5
TEXT_WIDTH = 29*8
PLAYER_SPEED = 100
PLAYER_SCRIPT_ID = '__PLAYER'
ROOM_WIDTH = 316
ROOM_HEIGHT = 166
FLAG_WALK_BLOCK = 16

class COLORS:
	WALKAREA = (0.8, 0.8, 0.8, 1)
	HOTSPOT = (0, 0, 1, 1)
	WHITE = (1,1,1,1)
	RED = monkey2.fromHex('#AA0000')


room = 'garden_east'
PLAYER_POS = [10, 10, 0]
PLAYER_DIR = 'n'
inventory_mode = 0
inventory = {
	#'carrot': 1,
	'sword': 1
}