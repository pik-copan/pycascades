class linear_coupling:
	def __init__(self,strength,out):
		self.strength = strength
		self.out = out
	
	def coupling(self):
		return self.strength*self.out.x
		
