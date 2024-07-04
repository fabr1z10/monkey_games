from . import data
from . import settings

def _startIn(room: str, pos: list):
    settings.room = room
    settings.characters = ['dave', 'bernard']
    settings.player = 0
    dave =data.items['items']['dave']
    dave['room'] = room
    dave['pos'] = pos

def test_chandelier():
    # open cabinet; use cassette tape in cassette player
    # turn on cassette player; wait for chandelier to break
    # turn off cassette player; pick up cassette tape;
    # pick up old rusty key
    _startIn('living', [50, 10])
    data.inventory['dave'] = ['cassette_tape']
    data.tape_recorded = 1
    dave =data.items['items']['dave']
    dave['direction'] = 'e'

def test_grating():
    _startIn('housefront', [300, 10])
    dave = data.items['items']['dave']
    dave['direction'] = 'e'

def test_pantry():
    _startIn('pantry', [50, 10])
    data.inventory['dave'] = ['silver_key']
    dave = data.items['items']['dave']
    dave['direction'] = 'e'


