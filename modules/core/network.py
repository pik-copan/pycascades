class network:
    
    def __init__(self):
        self.tip_list = []
        
    def add_element(self,tip_element):
        self.tip_list.append(tip_element)
        
    def system(self,x,t):
        df = []
        for tip_element in self.tip_list:
            df.append(tip_element.f_prime(x))
        return df
            
    def get_state(self):
        state_vec = []
        for tip_element in self.tip_list:
            state_vec.append(tip_element.x)
        return state_vec
        
    def get_structure(self):
        ret_string = ""
        for tip_element in self.tip_list:
            ret_string = ret_string + str(tip_element.id) + "\n"
        for cpl in tip_element.cpl_list:
            ret_string = (ret_string + str(cpl.out.id) 
                          + " --> " + str(tip_element.id)
				        + "\n")
        return ret_string
