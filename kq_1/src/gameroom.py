import monkey2

def baseRoom():
    room = monkey2.Room()


    room.setStartUpFunction(ciao)
    room.setClearColor((0, 0.2, 0.2))
    cam = monkey2.CamOrtho(256, 240)
    room.addCamera(cam)
    cam.setPosition([0,0,5], [0,0,-1], [0,1,0])

    batch = monkey2.QuadBatch(10, 0, 512, 512, 16)
    room.addBatch(batch)
    room.addBatch(monkey2.LineBatch(1000, 0))

    batch.addTexture('/home/fabrizio/monkey_games/adventure_demo/assets/kq1.png')
    monkey2.game().makeCurrent(room)

    graham = assetman.makeSprite('graham', 0)
    root = room.root()
    m = monkey2.Node()
    m.addComponent(monkey2.Follow(0))
    m.setModel(graham)
    root.add(m)


    n = monkey2.adventure.WalkArea([0,0,100,0,100,100,200,100,200,200,0,200],1)
    root.add(n)

    scheduler = monkey2.Scheduler()
    root.add(scheduler)

    c=monkey2.adventure.MouseController(0, n, m, scheduler, 50)
    root.add(c)


    return room
