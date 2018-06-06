class network:
	def __init__(self):
		self.tip_list = []
	def add_element(self,tip_element):
		self.tip_list.append(tip_element)
	def plot_net(self):
		ret_string = ""
		for tip_element in self.tip_list:
			ret_string = ret_string + str(tip_element.id) + "\n"
			for cpl in tip_element.cpl_list:
				ret_string = (ret_string + str(cpl.out.id) 
					      + " --> " + str(tip_element.id) 
					      + "\n")
		return ret_string
	def iterate(self,dt):
		for tip_element in self.tip_list:
			tip_element.iterate(dt)
		for tip_element in self.tip_list:
			tip_element.push_state()
	def get_state(self):
		ret_string = ""
		for tip_element in self.tip_list:
			ret_string = ret_string + str(tip_element.x) + " "
		return ret_string
