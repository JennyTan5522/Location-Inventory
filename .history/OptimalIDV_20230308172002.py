from SupplyChain import SupplyChain
from GA import GA
#Access with SC formula

class OptimalIDV:
    '''This class is used to find the optimal inventory decision variable (s,Q)'''
    def __init__(self):
        #TODO need initialize size at here !! -> sc,ga
        self.sc=SupplyChain('5-10','TYPE_II')
        self.GA=GA(10000,20,100,0.8,0.2,self.sc)
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
        optimalQS={'Q':0,'s':0}
        minTotalCost=100000
        for qm in range(len(Qmin)):
            #Make sure Qmin>0
            if Qmin[qm]>0 and qm==0: #TODO remove qm==0 just for testing
                for num in reversed(range(4,round(Qmin[qm]+1))):
                    #Ori=232, q=231, s=230
                    q=num-1
                    s=num-2
                    print(q)
                    print(s)
                    #Find optimal sj,qj until TC=0, sub sj and qj into the TC
                    #TODO is it need to loop thru population?
                    for i in range(self.GA.POP_SIZE):
                        population=self.GA.initialPopulation()
                        X=self.sc.generateX(population[i])
                        Y=self.generateY(self.X)
                        totalCost=self.sc.calcTotalCost(X,Y,s,q) #TODO X and Y how define?
                    # if(totalCost<minTotalCost):
                    #     minTotalCost=totalCost
                    #     optimalQS['Q']=Qmin[q]
                    #     optimalQS['s']=Qmin[s]

                    # if(totalCost==0):
                    #     optimalQS['Q']=Qmin[q]
                    #     optimalQS['s']=Qmin[s]
                    #     break
                        
                print('-----------------------------------')
    



idv=OptimalIDV()
Qmin=idv.calcQmin()
print(Qmin)
idv.calcOptimalSQ(Qmin)
# for num in reversed(range(4,round(10)+1)):
#     print(num)
#     q=num-1
#     s=num-2
#     print(q,s)

# Qmin=round(50.50)
# count=Qmin
# print(count)
# while(count!=0):
#     count-=1
#     print(count)
# x=(100-10)*20*(20+50)/(100*1)
# print(x)
#q1minCost=((100-10)*(20+self.sc.DC_ARRIVAL_RATE_2[j]))/(self.sc.HOLDING_COST[j]*self.sc.LEAD_TIME[j])