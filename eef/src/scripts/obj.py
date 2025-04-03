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

def pickup_key_main(id, _):
    pass