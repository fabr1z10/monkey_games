import monkey
import settings
from .gameroom import GameRoom

def init():
  print('fucami')
  settings.worlds = monkey.read_data_file('worlds.yaml')
  settings.strings = monkey.read_data_file('strings.yaml')
  settings.data = monkey.read_data_file('tiles.yaml')


def create_room():
  a = GameRoom()
  return a



  # get root





