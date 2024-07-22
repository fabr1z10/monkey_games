from . import data
from . import settings

def start():
    settings.room = 'start'
    settings.items['graham'].update({
        'room': 'start',
        'pos': [200, 40]
    })
