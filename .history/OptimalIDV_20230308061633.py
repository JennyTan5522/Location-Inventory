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
        qminCost=0
        print(self.sc.CUSTOMER_CLASS.keys())
        # for j in range(self.sc.NO_OF_DC):
        #     for r in range(self.sc.CUSTOMER_CLASS.keys()):
        #         if r==0: #Priority customer
        #             q1minCost=(self.sc.COST_LOSE_1-self.sc.PURCHASING_COST_UNIT[j])*(self.sc.DC_ARRIVAL_RATE_1[j]+self.sc.DC_ARRIVAL_RATE_2[j])/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])
        #         else: #Ordinary customer
        #             q1minCost=(self.sc.COST_LOSE_2-self.sc.PURCHASING_COST_UNIT[j])*(self.sc.DC_ARRIVAL_RATE_1[j]+self.sc.DC_ARRIVAL_RATE_2[j])/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])
        #     Qmin.append(qminCost)
        #     print(q1minCost)
        pass


idv=OptimalIDV()
idv.calcQmin()