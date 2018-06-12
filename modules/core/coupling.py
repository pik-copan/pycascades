class linear_coupling:
    def __init__(self,strength,out):
        self.strength = strength
        self.out = out
        
    def coupling(self,x):
        return self.strength*x
		
