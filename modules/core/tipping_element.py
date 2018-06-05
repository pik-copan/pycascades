class tipping_element:
	def __init__(self):
		pass
	def iterate(self,dt):
		pass

class cusp(tipping_element):

	def __init__(self,a,x):
		self.a = a
		self.x = x
	def iterate(self,dt):
		self.x = self.x + dt*self.dxdt()
	def dxdt(self):
		return -pow(self.x,3)+self.a*self.x
		
