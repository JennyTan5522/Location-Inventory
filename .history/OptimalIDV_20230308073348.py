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
        Qmin=[]
        for j in range(self.sc.NO_OF_DC):
            QminCost=0
            for r in range(len(self.sc.CUSTOMER_CLASS.keys())):
                if r==0: #Priority customer
                    QminCost=((self.sc.COST_LOSE_1-self.sc.PURCHASING_COST_UNIT[j])*self.sc.DC_ARRIVAL_RATE_1[j]*(self.sc.DC_ARRIVAL_RATE_1[j]+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])
                else: #Ordinary customer
                    QminCost=((self.sc.COST_LOSE_2-self.sc.PURCHASING_COST_UNIT[j])*self.sc.DC_ARRIVAL_RATE_1[j]*(self.sc.DC_ARRIVAL_RATE_1[j]+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])
                Qmin.append(QminCost) 
        print(Qmin)
        print('--------------------------------------------')
        return Qmin
    
    def calcOptimalSQ(self,Qmin:list):
        '''Step 2: Find optimal S0j, Q0j and costs'''
        for q in range(len(Qmin)):
            count=Qmin[q]
            for q_reversed in reversed(round(Qmin[q])):
                print(q_reversed)
        
        pass

    



idv=OptimalIDV()
Qmin=idv.calcQmin()
idv.calcOptimalSQ(Qmin)
# x=(100-10)*20*(20+50)/(100*1)
# print(x)
#q1minCost=((100-10)*(20+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])