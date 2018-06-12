class tipping_element:
    
    def __init__(self,id_number):
        self.id = id_number
        self.x = 0.0
        self.cpl_list = []
        
    def add_cpl(self,cpl):
        self.cpl_list.append(cpl)
        
    def cpl_sum(self,x):
        try: 
            self.cpl_list
        except AttributeError:
            return 0.0
        else:
            ret_sum = 0.0
            for cpl in self.cpl_list:
                ret_sum = ret_sum + cpl.coupling(x[cpl.out.id])
        return ret_sum
        
    def dxdt(self):
        print ("Warning: Either using abstract tipping_element class which"
                 + "is not suggested or forgot to override dxdt() function")
        return 0.0
    
    def f_prime(self,x):
        return ( self.dxdt(x[self.id]) + self.cpl_sum(x) )
    
    def update_state(self,x):
        self.x = x

class cusp(tipping_element):
    
    def __init__(self, id_number, a, b, c):
        tipping_element.__init__(self,id_number)
        self.a = a
        self.b = b
        self.c = c
        
    def dxdt(self,x):
        return ( self.a*pow(x,3) + self.b*x + self.c )
