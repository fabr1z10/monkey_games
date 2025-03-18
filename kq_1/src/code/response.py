import monkey2
from monkey2 import Vec3
from .. import state


class GoToRoom(monkey2.CollisionResponse):
	def onStart(self, player, hotspot):
		state.room = hotspot.userData['room']
		x = hotspot.userData.get('x', player.x)
		y = hotspot.userData.get('y', player.y)
		state.PLAYER_POS = Vec3(x, y, 0)
		state.PLAYER_DIR = hotspot.userData['dir']
		monkey2.closeRoom()

# collision with water areas
class Swim(monkey2.CollisionResponse):
	def onStart(self, player, hotspot):
		player.setModel(monkey2.getModel('main/graham-swim'))

	def onEnd(self, player, hotspot):
		player.setModel(monkey2.getModel('main/graham'))