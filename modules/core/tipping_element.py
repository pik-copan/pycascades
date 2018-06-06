class tipping_element:
	def __init__(self):
		self.x = 0
	def iterate(self,dt):
		pass

class cusp(tipping_element):

	def __init__(self,x,a):
		self.x = x
		self.a = a
	def iterate(self,dt):
		self.x = self.x + dt*self.dxdt()
	def dxdt(self):
		return -pow(self.x,3)+self.a*self.x
		
