from SupplyChain import SupplyChain
#Access with SC formula

class OptimalIDV:
    '''This class is used to find the optimal inventory decision variable (s,Q)'''
    def __init__(self):
        #TODO need initialize size at here !!
        self.sc=SupplyChain('5-10','TYPE_II')
        pass
    
    def calcqMin(self):
        '''Step 1: Calculate qMin for each DC'''
        qMin=[]
        for j in range(self.sc.NO_OF_DC):
            qMinCost=0
            for r in range(len(self.sc.CUSTOMER_CLASS.keys())):
                if r==0: #Priority customer
                    qMinCost=((self.sc.COST_LOSE_1-self.sc.PURCHASING_COST_UNIT[j])*self.sc.DC_ARRIVAL_RATE_1[j]*(self.sc.DC_ARRIVAL_RATE_1[j]+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])
                else: #Ordinary customer
                    qMinCost=((self.sc.COST_LOSE_2-self.sc.PURCHASING_COST_UNIT[j])*self.sc.DC_ARRIVAL_RATE_1[j]*(self.sc.DC_ARRIVAL_RATE_1[j]+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])
                qMin.append(qMinCost) 
            print('--------------------------------------------')
        print(qMin)
        return qMin
    
    def calcOptimalSQ(self,qMin:list):
        '''Step 2: Find optimal S0j, Q0j and costs'''
        for 
        for q in reversed(range(2,len(qMin))):
            print(qMin[q])
        
        pass

    



idv=OptimalIDV()
qMin=idv.calcqMin()
idv.calcOptimalSQ(qMin)
# x=(100-10)*20*(20+50)/(100*1)
# print(x)
#q1minCost=((100-10)*(20+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])