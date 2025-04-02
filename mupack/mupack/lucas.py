import monkey2
from monkey2 import Color

from . import assets
from .util import add_tag, get_tag
from .yaml_reader import eval_string

def updateActionLabel():
    verb = assets.verbs[0][assets.state.action]
    print('obj1=',assets.state.object1)
    s = eval_string(verb.text)
    if assets.state.object1:
        print(assets.items[assets.state.object1])
        s += " " + eval_string(assets.items[assets.state.object1]['text'])

    get_tag('LABEL_ACTION').updateText(s)


class VerbHotSpot(monkey2.HotSpot):
    def __init__(self, shape, camera, key):
        self.key = key
        super().__init__(shape, 0, camera)

    def onEnter(self):
        self.node.setMultiplyColor(Color(assets.state._color_verb_active))

    def onLeave(self):
        self.node.setMultiplyColor(Color(assets.state._color_verb_inactive))

    def onClick(self, pos):
        assets.state.action = self.key
        assets.state.object1 = None
        assets.state.object2 = None
        updateActionLabel()


def create_UI(root, verbSet: int):
    for key, value in assets.verbs[verbSet].items():
        t = monkey2.Text('uimain/c64',
            eval_string(value.text), monkey2.Color(assets.state._color_verb_inactive))
        shape = monkey2.shapes.Rect(t.size.x, t.size.y, anchor=monkey2.Vec2(0,1))
        hotspot = VerbHotSpot(shape, 1, key)
        t.addComponent(hotspot)
        t.setPosition(monkey2.Vec3(*value.pos))
        snode = monkey2.Node()
        snode.setModel(shape.toModel(monkey2.ModelType.WIRE), 3)
        snode.setMultiplyColor(monkey2.Color(assets.state._color_verb_inactive))
        t.add(snode)
        root.add(t)
    # create action label
    al = monkey2.Text('uimain/c64',
        eval_string(assets.verbs[verbSet][assets.state._default_verb].text),
        Color(assets.state._color_action))
    al.setPosition(monkey2.Vec3(2, 55, 0))
    add_tag('LABEL_ACTION', al)
    assets.state.action = assets.state._default_verb
    root.add(al)


class LucasObjectHotSpot(monkey2.HotSpot):
    def __init__(self, itemId: str, shape, priority, camera):
        super().__init__(shape, priority, camera)
        self.item_id = itemId

    def onEnter(self):
        if assets.state.object1:
            assets.state.object2 = self.item_id
        else:
            assets.state.object1 = self.item_id
        updateActionLabel()

    def onLeave(self):
        if assets.state.object2:
            assets.state.object2 = None
        else:
            assets.state.object1 = None
        updateActionLabel()

    def onClick(self, pos):
        action = assets.state.action

        if assets.state.object2:
            aid = f"{action}_{assets.state.object1}_{assets.state.object2}"
        else:
            aid = f"{action}_{assets.state.object1}"
        print('action id: ', aid)
        # try to see if I have script
        af = getattr(assets.scripts, aid, None)
        if af:
            print('found')
        else:
            print('not found - try default action for ',action)
            af = getattr(assets.scripts, '_' + action, None)
            if af:
                af(assets.state.object1, assets.state.object2)
            else:
                print(' -- nothing found.')

