import monkey2
from . import code
from . import state

from .util import exit_with_err



class ObjectHotSpot(monkey2.HotSpot):
    def __init__(self, data, shape, priority, camera):
        super().__init__(shape, priority, camera)
        self.data = data
        self.actions = data['hotspot'].get('actions', {})

    def onEnter(self):
        pass

    def onLeave(self):
        pass

    def onClick(self, pos):
        action = self.actions.get(state.action, None)
        if action:
            f = getattr(code, action[0], None)
            if not f:
                exit_with_err(f' ERROR: function "{action[0]}" not found')
            args = action[1] if len(action)>1 else {}
            f(self, **args)
        else:
            if state.action == 'walk':
                turn = None
                if 'walk_to' in self.data:
                    pos = self.data['walk_to']
                    turn = self.data.get('turn', None)
                code.walk_player_to(pos, turn=turn)
            else:
                # print a default message
                code.message(self, text=8)
                #print(f'No "{state.action}" defined.')