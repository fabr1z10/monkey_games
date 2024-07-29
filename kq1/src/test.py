from . import data
from . import settings
from . import utils

def set_player(room: str, pos: list):
    settings.room = room
    utils.moveTo('graham', room)
    settings.getItem('graham').update({
        'pos': pos
    })


def start():
    set_player('room_start', [200, 40])


def rock():
    set_player('room_rock', [200, 40])
