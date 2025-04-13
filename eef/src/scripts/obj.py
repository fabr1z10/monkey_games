import mupack
import monkey2
from .a import walkScript, play

def pull_door_mat(id, _):
    script = monkey2.Script('__PLAYER')
    walkScript(script, 'PLAYER', id)
    mat = mupack.get_tag(id)
    if mat.animation == 'closed':
        mupack.assets.items[id]['state'] = 1
        hs = mat.getComponent('HOTSPOT')
        script.addAction(monkey2.actions.Animate(mat, 'open'))
        script.addAction(monkey2.actions.CallFunc(lambda: hs.setShape(monkey2.shapes.Rect(40, 8))))
    play(script)

def push_door_mat(id, _):
    script = monkey2.Script('__PLAYER')
    walkScript(script, 'PLAYER', id)
    mat = mupack.get_tag(id)
    if mat.animation == 'open':
        mupack.assets.items[id]['state'] = 0
        hs = mat.getComponent('HOTSPOT')
        script.addAction(monkey2.actions.Animate(mat, 'closed'))
        script.addAction(monkey2.actions.CallFunc(lambda: hs.setShape(monkey2.shapes.Rect(88, 8))))
    play(script)



def AddToInventory(id):
    def f():
        mupack.get_tag(id).remove()
        mupack.assets.items[id]['active'] = False
        mupack.assets.items[mupack.assets.state.player]['inventory'].append([id, 1])
        mupack.lucas.draw_inventory()
    return f


# the basic pickup - walk to the item,
# grab it (remove it), add to inventory
def pickup_base(id, _):
    script = monkey2.Script('__PLAYER')
    walkScript(script, 'PLAYER', id)
    script.addAction(monkey2.actions.CallFunc(AddToInventory(id)))
    play(script)

pickup_key_main = pickup_base