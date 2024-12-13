import monkey
from . import settings
from . import item_builders
from .gameroom import GameRoom

def init():
  settings.worlds = monkey.read_data_file('worlds.yaml')
  settings.strings = monkey.read_data_file('strings.yaml')


def create_room():
  a = GameRoom()
  return a



  # get root





