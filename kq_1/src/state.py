import monkey2

from monkey2 import Color, Vec3

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
PLAYER_SPEED = 100.0
PLAYER_SCRIPT_ID = '__PLAYER'
ROOM_WIDTH = 316
ROOM_HEIGHT = 166
FLAG_WALK_BLOCK = 16

class COLORS:
	WALKAREA = Color(0.8, 0.8, 0.8, 1)
	HOTSPOT = Color(0, 0, 1, 1)
	WHITE = Color(1, 1, 1, 1)
	RED = Color('#AA0000')


room = 'elf'
PLAYER_POS = Vec3(10, 10, 0)
PLAYER_DIR = 'n'
inventory_mode = 0
inventory = {
	#'carrot': 1,
	'sword': 1
}