import monkey2


IDS = {}

scheduler = None

def getNode(s: str):
	return monkey2.getNode(IDS[s])


ROOM_WIDTH = 316
ROOM_HEIGHT = 166
WALKAREA_COLORS = [
	(1,1,1,1),
	(1,0,0,1)
]
room = 'start'