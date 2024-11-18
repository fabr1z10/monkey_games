import monkey
from . import settings
from .room import GameRoom

def init():
	settings.level_data = monkey.read_data_file('bblevels.yaml')


def create_room():
    room = GameRoom()
    return room
