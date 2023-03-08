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
        return Qmin
    
    def calcOptimalSQ(self,Qmin:list):
        '''Step 2: Find optimal S0j, Q0j and costs'''
        for qm in range(len(Qmin)):
            #Make sure Qmin>0
            if Qmin[qm]>0 and qm==0: #TODO remove qm==0 just for testing
                for num in reversed(range(2,round(Qmin[qm]+1))):
                    #Ori=232, q=231, s=230
                    q=num-1
                    s=num-2
                    print(q,s)
                    #Find optimal sj,qj until TC=0, sub sj and qj into the TC
                    
                    #s=
                    
                    #totalCost=self.sc.calcTotalCost(X,Y,s,Q)
                print('-----------------------------------')
    



idv=OptimalIDV()
Qmin=idv.calcQmin()
print(Qmin)
#idv.calcOptimalSQ(Qmin)
for num in reversed(range(2,round(10))):

# Qmin=round(50.50)
# count=Qmin
# print(count)
# while(count!=0):
#     count-=1
#     print(count)
# x=(100-10)*20*(20+50)/(100*1)
# print(x)
#q1minCost=((100-10)*(20+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])