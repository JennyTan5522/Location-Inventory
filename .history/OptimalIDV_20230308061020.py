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
        QMin=[]
        q1MinCost=0
        for j in range(self.sc.NO_OF_DC):
            for r in range(self.sc.CUSTOMER_CLASS):
                if r==0: #Priority customer
                    q1MinCost=self.sc.COST_LOSE_1-self.sc.PURCHASING_COST_UNIT[j]
                    pass
                else: #Ordinary customer
                    pass

            Q1Min.append()
        pass


idv=OptimalIDV()
idv.calcQmin()