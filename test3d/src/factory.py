import monkey

from .legomodel import LegoModel, initialize


#LEGO_MODEL = '35c01.dat'
LEGO_MODEL='48/1-4cyli.dat'
LEGO_MODEL='4-4cyli.dat'
LEGO_MODEL='stud.dat'
p = 0
def move_cam(cam, by):
	def f():
		cam.move(by)
	return f

def toggle_cam(cam):
	def f():
		global p
		if p == 0:
			cam.set_position([0, 5, 0], (0, -1, 0), (0, 0, -1))
			p = 1
		else:
			cam.set_position([0, 8, 5], (0, 0, -1), (0, 1, 0))
			p = 0
	return f

def create_room():
	room = monkey.Room()
	cam = monkey.CamPerspective()
	room.add_camera(cam)
	room.add_batch('lines', monkey.LineBatch(max_elements=2000, cam=0))
	room.add_batch('tri', monkey.TriangleBatch(max_elements=10000, cam=0))
	monkey.engine().setCurrentRoom(room)
	cam.set_position([0, 0, 5], (0, 0, -1), (0, 1, 0))
	cam.set_position([0, 5, 0], (0, -1, 0), (0, 0, -1))

	initialize()
	lm = LegoModel(LEGO_MODEL)
	#print(lm)
	#n = monkey.Node()
	# open LDConfig.ldr


	#m = monkey.models.LineModel('lines', color=(1, 0, 0, 1), points=[0, 0, 0, 20, 0, 0])
	#m = monkey.models.TriangleModel('tri', color =(1,0,0,1), points= [0,0,0,1,0,0,0.5,0.5,0])
	#n.set_model(m)
	root = room.root()
	#root.add(n)

	k = lm.instantiate()
	#k.setTransform([6,0,0,0, 0,-4,0,0, 0,0,6,0, 0,0,0,0])
	root.add(k)

	kb = monkey.components.Keyboard()
	kb.add(265, 1, 0, move_cam(cam, (0, 0, -0.1)))
	kb.add(265, 2, 0, move_cam(cam, (0, 0, -0.1)))
	kb.add(264, 1, 0, move_cam(cam, (0, 0, 0.1)))
	kb.add(264, 2, 0, move_cam(cam, (0, 0, 0.1)))
	kb.add(262, 1, 0, move_cam(cam, (0.1, 0, 0)))
	kb.add(262, 2, 0, move_cam(cam, (0.1, 0, 0)))
	kb.add(263, 1, 0, move_cam(cam, (-0.1, 0, 0)))
	kb.add(263, 2, 0, move_cam(cam, (-0.1, 0, 0)))
	kb.add(81, 1, 0, toggle_cam(cam))
	root.add_component(kb)

	return room
