import monkey

def makeWalkableCollider(outline):
    c = monkey.Node()
    c.add_component(monkey.components.Collider(2, 0, 0, monkey.shapes.Polygon(outline), batch='lines'))
    return c
