import monkey2

import lego


def create_room():

    lego.initialize()


    room = monkey2.Room()
    cam = monkey2.CamPerspective()
    room.addCamera(cam)
    cam.setPosition([0,2,5], [0,0,-1], [0,1,0])

    room.addBatch(monkey2.LineBatch(100, 0))
    room.addBatch(monkey2.TriangleBatch(100, 0))
    nb = monkey2.TriangleNormalBatch(10000, 0)
    nb.addLight(monkey2.DirectionalLight((-1, -1, -1), (1,1,1), 0.2))
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
    n3.addComponent(monkey2.CamControl3D(0,5,2))
    root.add(n3)

    lm = lego.LegoModel('4-4cyli.dat')
    k = lm.instantiate()
    root.add(k)


    return room
