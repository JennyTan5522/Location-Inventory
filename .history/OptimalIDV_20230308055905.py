from SupplyChain import SupplyChain
#Access with SC formula

class OptimalIDV:
    '''This class is used to find the optimal inventory decision variable (s,Q)'''
    def __init__(self):
        self.sc=SupplyChain()
        pass
    
    def calcQmin(self):
        '''Step 1: Calculate Qmin for each DC'''
        for j in range(self.sc.self.NO_OF_DC):
            print(self.sc.self.NO_OF_DC[j])
        pass


idv=OptimalIDV()
idv.calcQmin()