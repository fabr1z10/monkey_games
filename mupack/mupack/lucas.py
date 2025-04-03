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


class ArrowUpHotSpot(monkey2.HotSpot):
    def __init__(self, shape, camera, batch):
        self.batch = batch
        super().__init__(shape, 0, camera, batch)

    def onEnter(self):
        self.node.setMultiplyColor(Color(assets.state._color_inv_active))

    def onLeave(self):
        self.node.setMultiplyColor(Color(assets.state._color_inv_inactive))

    def onClick(self, pos):
        print('MANAGIAlPAUTANA')
        assets.items[assets.state.player]['inventory_offset'] -= 2
        draw_inventory(self.batch)

class ArrowDownHotSpot(monkey2.HotSpot):
    def __init__(self, shape, camera, batch):
        self.batch = batch
        super().__init__(shape, 0, camera, batch)

    def onEnter(self):
        self.node.setMultiplyColor(Color(assets.state._color_inv_active))

    def onLeave(self):
        self.node.setMultiplyColor(Color(assets.state._color_inv_inactive))

    def onClick(self, pos):
        print('FOUDDD')
        assets.items[assets.state.player]['inventory_offset'] += 2
        draw_inventory(self.batch)



class InventoryHotSpot(monkey2.HotSpot):
    def __init__(self, shape, camera, key, batch):
        self.key = key
        super().__init__(shape, 0, camera, batch)

    def onEnter(self):
        self.node.setMultiplyColor(Color(assets.state._color_inv_active))

    def onLeave(self):
        self.node.setMultiplyColor(Color(assets.state._color_inv_inactive))

    def onClick(self, pos):
        pass

class VerbHotSpot(monkey2.HotSpot):
    def __init__(self, shape, camera, key, batch):
        self.key = key
        super().__init__(shape, 0, camera, batch)

    def onEnter(self):
        self.node.setMultiplyColor(Color(assets.state._color_verb_active))

    def onLeave(self):
        self.node.setMultiplyColor(Color(assets.state._color_verb_inactive))

    def onClick(self, pos):
        assets.state.action = self.key
        assets.state.object1 = None
        assets.state.object2 = None
        updateActionLabel()


def draw_inventory(batchId):
    inv_root = get_tag('INVENTORY')
    inv_root.clear()
    inv = assets.items[assets.state.player]['inventory']
    inv_offset = assets.items[assets.state.player]['inventory_offset']
    print(' ************** REDRAW INV AT ',inv_offset)
    arrow_up = inv_offset > 0
    arrow_down = inv_offset + 4 <= len(inv)
    for i in range(0, 4):
        if inv_offset + i >= len(inv):
            break
        anchor = monkey2.Vec2(0,0) if i%2==0 else monkey2.Vec2(1,0)
        inv_item = monkey2.Text('uimain/c64',
            inv[inv_offset+i][0],
            Color(assets.state._color_inv_inactive),anchor=anchor)
        x = 2 if i % 2 == 0 else 318
        y = 23 - 8 * (i // 2)
        inv_item.setPosition(monkey2.Vec3(x, y, 0))
        shape = monkey2.shapes.Rect(inv_item.size.x, inv_item.size.y,
                                    anchor=monkey2.Vec2(anchor.x,1))
        hotspot = InventoryHotSpot(shape, 1,  inv[inv_offset+i][0], batchId)
        inv_item.addComponent(hotspot)
        inv_root.add(inv_item)
    if arrow_down:
        adown = monkey2.Node()
        adown.setModel(monkey2.getModel('uimain/arrow_down'))
        hotspot = ArrowDownHotSpot(
            monkey2.shapes.Rect(12,8, anchor=monkey2.Vec2(0.5,0)),
        1,
            batchId)
        adown.addComponent(hotspot)
        adown.setPosition(monkey2.Vec3(160, 8, 0))
        inv_root.add(adown)
    if arrow_up:
        aup = monkey2.Node()
        aup.setModel(monkey2.getModel('uimain/arrow_up'))
        hotspot2 = ArrowUpHotSpot(
            monkey2.shapes.Rect(12,8, anchor=monkey2.Vec2(0.5,0)),
        1,
            batchId)
        aup.addComponent(hotspot2)
        aup.setPosition(monkey2.Vec3(160, 16, 0))
        inv_root.add(aup)

def create_UI(root, verbSet: int, batchId):
    for key, value in assets.verbs[verbSet].items():
        t = monkey2.Text('uimain/c64',
            eval_string(value.text), monkey2.Color(assets.state._color_verb_inactive))
        shape = monkey2.shapes.Rect(t.size.x, t.size.y, anchor=monkey2.Vec2(0,1))
        hotspot = VerbHotSpot(shape, 1, key, batchId)
        t.addComponent(hotspot)
        t.setPosition(monkey2.Vec3(*value.pos))
        #snode = monkey2.Node()
        #snode.setModel(shape.toModel(monkey2.ModelType.WIRE), 3)
        #snode.setMultiplyColor(monkey2.Color(assets.state._color_verb_inactive))
        #t.add(snode)
        root.add(t)
    # create action label
    al = monkey2.Text('uimain/c64',
        eval_string(assets.verbs[verbSet][assets.state._default_verb].text),
        Color(assets.state._color_action))
    al.setPosition(monkey2.Vec3(2, 55, 0))
    add_tag('LABEL_ACTION', al)
    assets.state.action = assets.state._default_verb
    root.add(al)
    # items held by player
    inventory = monkey2.Node()
    root.add(inventory)
    add_tag('INVENTORY', inventory)
    draw_inventory(batchId)


    # create inventory items



class LucasObjectHotSpot(monkey2.HotSpot):
    def __init__(self, itemId: str, shape, priority, camera, batch):
        super().__init__(shape, priority, camera, batch)
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
            af(assets.state.object1, assets.state.object2)
        else:
            print('not found - try default action for ',action)
            af = getattr(assets.scripts, '_' + action, None)
            if af:
                af(assets.state.object1, assets.state.object2)
            else:
                print(' -- nothing found.')

