from SupplyChain import SupplyChain
#Access with SC formula

class OptimalIDV:
    '''This class is used to find the optimal inventory decision variable (s,Q)'''
    def __init__(self):
        #TODO need initialize size at here !!
        self.sc=SupplyChain('5-10','TYPE_II')
        pass
    
    def calcQmin(self):
        '''Step 1: Calculate Qmin for each DC'''
        Q1Min=[]
        for j in range(self.sc.NO_OF_DC):
            print(j)
            q1MinCost=0
            for r in range(self.sc.CUSTOMER_CLASS):
                if r==0: #Priority customer
                    pass
                else: #Ordinary customer
                    pass

            Q1Min.append()
        pass


idv=OptimalIDV()
idv.calcQmin()