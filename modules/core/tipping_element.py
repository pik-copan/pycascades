class tipping_element:
    
	def __init__(self,id_number):
		self.id = id_number
		self.x = 0.0
		self.cpl_list = []
        
	def add_cpl(self,cpl):
		self.cpl_list.append(cpl)
        
	def cpl_sum(self):
		try: 
    			self.cpl_list
		except AttributeError:
    			return 0.0
		else:
			ret_sum = 0.0
			for linear_coupling in self.cpl_list:
				ret_sum = ret_sum + linear_coupling.coupling()
			return ret_sum 
        
	def dxdt(self):
		print ("Warning: Either using abstract tipping_element class which"
                 + "is not suggested or forgot to override dxdt() function")
		return 0.0
    
	def f_prime(self):
		return ( self.dxdt() + self.cpl_sum() )
    
	def push_state(self):
		self.x = self.x_new

class cusp(tipping_element):
    
	def __init__(self, id_number, x, a):
		tipping_element.__init__(self,id_number)
		self.x = x
		self.a = a
        
	def dxdt(self):
		return -pow(self.x,3)+self.a*self.x
