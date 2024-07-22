import monkey
from . import scripts
from . import settings

def makeWalkableCollider(outline):
    c = monkey.Node()
    c.add_component(monkey.components.Collider(2, 0, 0, monkey.shapes.Polygon(outline), batch='lines'))
    return c

def readShape(data):
    if 'path' in data:
        s = monkey.shapes.PolyLine(data['path'])
    elif 'poly' in data:
        s = monkey.shapes.Polygon(data['poly'])
    return s

def makeCollider(data, shape=None):
    if not shape:
        shape = readShape(data)
    collideMask = data.get('mask', settings.CollisionFlags.player)
    collider = monkey.components.Collider(settings.CollisionFlags.hotspot,
        collideMask, 10, shape, batch='lines')
    for c in data['response']:
        f = getattr(scripts, c['on_enter'][0])(**c['on_enter'][1])
        collider.setResponse(c['tag'], on_enter=f)
    return collider

def makeScoreBar():
    menu_node = monkey.Node()
    menu_bar = monkey.Node()
    menu_bar.set_model(monkey.models.from_shape('tri2', monkey.shapes.AABB(0, 320, 0, 8),
        settings.Colors.White, monkey.FillType.Solid))
    menu_bar.set_position(0,192,0)
    menu_node.add(menu_bar)
    score_label = monkey.Text(batch='ui', font='sierra', text='Ciao', anchor=monkey.ANCHOR_BOTTOMLEFT, pal='black')
    score_label.set_position(8, 0, 0)
    sound_label = monkey.Text(batch='ui', font='sierra', text='Ciao', anchor=monkey.ANCHOR_BOTTOMLEFT, pal='black')
    sound_label.set_position(240, 0, 0)
    menu_bar.add(score_label)
    menu_bar.add(sound_label)
    return menu_node