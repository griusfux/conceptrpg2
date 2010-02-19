# $Id$

# Description: Wraps a KX_GameObject to be used with the system
# Contributers: Mitchell Stokes

# Movement modes
MOVE_LINV = 0
MOVE_FORCE = 1
MOV_LOC = 2
MOV_SERVO = 3
MOV_POS = 4

class BlenderObjectWrapper:
	"""KX_GameObject wrapper"""
	
	def __init__(self, gameobj):
		self.gameobj = gameobj
		
	def Move(self, vec, mode=MOVE_LINV, local=True):
		"""Do object movement"""
		
		if mode == MOVE_LINV:
			self.gameobj.setLinearVelocity(vec, local)
		elif mode == MOVE_FORCE:
			self.gameobj.applyForce(vec, local)
		elif mode == MOVE_LOC:
			self.gameobj.applyMovement(vec, local)
		elif mode == MOVE_SERVO:
			self.gameobj.applyForce(vec, local)
		elif mode == MOVE_POS:
			self.gameobj.position = vec
		else:
			raise ValueError("Supplied mode is invalid!")
			
	def Rotate(self, vec, local=True):
		"""Do object rotation"""
		
		self.gameobj.applyRotation(vec, local)