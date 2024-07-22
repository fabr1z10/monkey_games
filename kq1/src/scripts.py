import monkey

def restart_room():
    monkey.close_room()

def drown(**kwargs):
    def f(hotspot, player):
        print('SUCA 4')
        x = kwargs.get('x', player.x)
        y = kwargs.get('y', player.y)
        script = monkey.Script()
        script.add(monkey.actions.SierraEnable(id=player.id, value=False))
        script.add(monkey.actions.Move(id=player.id, position=(x, y, 1 - y / 166), speed=0))
        script.add(monkey.actions.Animate(id=player.id, anim='drown'))
        monkey.play(script)
    return f
