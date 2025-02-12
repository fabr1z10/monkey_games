import monkey2

import lego


def create_room():

    lego.initialize()


    room = monkey2.Room()
    room.setClearColor((0,0.8,0.8))
    cam = monkey2.CamPerspective(far=1000)
    room.addCamera(cam)
    cam.setPosition([0,20,0], [0,0,-1], [0,1,0])
    #cam.setPosition([0,80,0], [0,-1,0], [0,0,1])

    room.addBatch(monkey2.LineBatch(100000, 0))
    room.addBatch(monkey2.TriangleBatch(10, 0))
    nb = monkey2.TriangleNormalBatch(200000, 0)
    nb.addLight(monkey2.DirectionalLight((-1, -1, -1), (1,1,1), 0.4))
    room.addBatch(nb)

    root = room.root()

    # n = monkey2.Node()
    # model = monkey2.LineModel([
    #     0,0,0, 1,0,0, 1,0,0,1,
    #     1,0,0, 1,1,0, 1,0,0,1,
    #     1,1,0, 0,0,0, 1,0,0,1])
    # n.setModel(model, 0)
    # root.add(n)
    #
    # n2 = monkey2.Node()
    # model2 = monkey2.TriangleModel([-1,0,0,0,0,0,-1,1,0,1,0,0,1])
    # n2.setModel(model2, 1)
    # root.add(n2)

    # n4 = monkey2.Node()
    # model3 = monkey2.TriangleNormalModel([-2,0,0,-1,0,0,-2,1,0,0,1,0,1,-1,0,0,-1,1,0,-2,1,0,0,0,1,1])
    # n4.setModel(model3, 2)
    # root.add(n4)

    n3 = monkey2.Node()
    n3.addComponent(monkey2.CamControl3D(0,20,2))
    root.add(n3)

    lm = lego.LegoModel('police.dat')
    k = lm.instantiate()
    scale=0.2
    root.setTransform([scale,0,0,0, 0,scale,0,0, 0,0,scale,0, 0,0,0,1])
    root.add(k)


    return room
