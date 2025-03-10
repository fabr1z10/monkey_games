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
TEXT_MARGIN_X = 10
TEXT_MARGIN_Y = 5
TEXT_WIDTH = 29*8
PLAYER_SPEED = 100
PLAYER_SCRIPT_ID = '__PLAYER'
ROOM_WIDTH = 316
ROOM_HEIGHT = 166
FLAG_WALK_BLOCK = 16
WALKAREA_COLORS = [
	(1,1,1,1),
	(1,0,0,1)
]
room = 'garden_east'
PLAYER_POS = [10, 10, 0]