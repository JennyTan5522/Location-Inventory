import yaml
import random
import numpy as np

class SupplyChain:
    random.seed(42)
    def __init__(self,PROBLEM_SIZE,SITUATION_TYPE):
        number_probSize=[]
        cost_list=[]
        #Load yaml file
        with open('PARAMETERS_INITIALIZATION.yml','r') as f:
            PARAMETERS_INITIALIZATION=yaml.safe_load(f)
        #======================================================================================================
        #Find problem size and initialize each number of Suppliers, DCs and Retailers
        for i in range(len(PARAMETERS_INITIALIZATION['PROBLEM_SIZE'])):
            #Loop for each size (SMALL,MEDIUM,LARGE)
            for size in PARAMETERS_INITIALIZATION['PROBLEM_SIZE'][i]:
                #Loop for size's values
                for size_value in PARAMETERS_INITIALIZATION['PROBLEM_SIZE'][i][size]:
                    #Extract number from size's values
                    if (size_value==PROBLEM_SIZE): #Means the value inside
                        #Loop for No fo Suppliers, DCs and retailers
                        number_probSize=PARAMETERS_INITIALIZATION['PROBLEM_SIZE'][i][size][size_value]
                        break      
        #======================================================================================================
        #Find cost based on situation type                
        for i in range(len(PARAMETERS_INITIALIZATION['SITUATION_TYPE'])):
            #Loop through each type
            for cost_types in PARAMETERS_INITIALIZATION['SITUATION_TYPE'][i]:
                if (cost_types==SITUATION_TYPE):
                    cost_list=PARAMETERS_INITIALIZATION['SITUATION_TYPE'][i][cost_types]
                    break
        #======================================================================================================        
        #Problem size initialization          
        self.NO_OF_SUPPLIER=number_probSize[0]
        self.NO_OF_DC=number_probSize[1]
        self.NO_OF_RETAILER=number_probSize[2]

        #Create a cost list, assign a random value based on the cost range of SITUATION_TYPE for each DC
        self.SETUP_COST=[random.randint(cost_list['SETUP_COST'][0],cost_list['SETUP_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.HOLDING_COST=[random.randint(cost_list['HOLDING_COST'][0],cost_list['HOLDING_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.PURCHASING_COST_UNIT=[random.randint(cost_list['PURCHASING_COST_UNIT'][0],cost_list['PURCHASING_COST_UNIT'][1]) for _ in range(self.NO_OF_DC)]
        self.LEAD_TIME=[random.randint(cost_list['LEAD_TIME'][0],cost_list['LEAD_TIME'][1]) for _ in range(self.NO_OF_DC)]
        self.FIXED_SHIPPING_COST=[random.randint(cost_list['FIXED_SHIPPING_COST'][0],cost_list['FIXED_SHIPPING_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.FIXED_COST=[random.randint(cost_list['FIXED_COST'][0],cost_list['FIXED_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.COST_LOSE_1=cost_list['COST_LOSE_1']
        self.COST_LOSE_2=cost_list['COST_LOSE_2']
        self.CUSTOMER_CLASS={'1':'PRIORITY','2':'ORDINARY'}
        self.RETAILER_ARRIVAL_RATE_1=[random.randint(cost_list['RETAILER_ARRIVAL_RATE'][0],cost_list['RETAILER_ARRIVAL_RATE'][1]) for _ in range(self.NO_OF_RETAILER)]
        self.RETAILER_ARRIVAL_RATE_2=[random.randint(cost_list['RETAILER_ARRIVAL_RATE'][0],cost_list['RETAILER_ARRIVAL_RATE'][1]) for _ in range(self.NO_OF_RETAILER)]
        
        self.SHIPPING_COST=np.zeros((self.NO_OF_RETAILER,self.NO_OF_DC)).astype('int')
        for j in range(self.NO_OF_DC):
            for i in range(self.NO_OF_RETAILER):
                self.SHIPPING_COST[i][j]=random.randint(cost_list['SHIPPING_COST'][0],cost_list['SHIPPING_COST'][1])

        #Compare the random arrival rate of both priority and ordinary customer then put the less arrival rate into priority customer
        for i in range(self.NO_OF_RETAILER):
            if(self.RETAILER_ARRIVAL_RATE_2[i]<self.RETAILER_ARRIVAL_RATE_1[i]):#If dc arrival rate 2 fast than 1 then swap place
                temp=self.RETAILER_ARRIVAL_RATE_1[i]
                self.RETAILER_ARRIVAL_RATE_1[i]=self.RETAILER_ARRIVAL_RATE_2[i]
                self.RETAILER_ARRIVAL_RATE_2[i]=temp

        #TODO arrival rate priority n ordinary rate
        #self.DC_ARRIVAL_RATE_1,self.DC_ARRIVAL_RATE_2=self.dcArrivalRate() #TODO how to pass X?

        print('Number of suppliers : ',self.NO_OF_SUPPLIER)
        print('Number of DCs       : ',self.NO_OF_DC)
        print('Number of retailers : ',self.NO_OF_RETAILER)
        print('                   Costs Listing')
        print('=============================================================')
        print('Setup cost                       : ',self.SETUP_COST)
        print('Holding cost                     : ',self.HOLDING_COST)
        print('Purchasing cost                  : ',self.HOLDING_COST)
        print('Shipping cost                    : ',self.SHIPPING_COST)
        print('Lead time                        : ',self.LEAD_TIME)
        print('Fixed Shipping cost              : ',self.FIXED_SHIPPING_COST)
        print('Retailer arrival rate priority   : ',self.RETAILER_ARRIVAL_RATE_1)
        print('Retailer arrival rate ordinary   : ',self.RETAILER_ARRIVAL_RATE_2)
        print('Fixed cost                       : ',self.FIXED_COST)
        print('Cost losing priority customer    : ',self.COST_LOSE_1)
        print('Cost losing ordinary customer    : ',self.COST_LOSE_2)


    def dcArrivalRate(self,X):
        '''Find DC arrival rate based on retailer arrival rate'''
        retailerArrivalRate1=np.reshape(self.RETAILER_ARRIVAL_RATE_1,(1,self.NO_OF_RETAILER))
        dcArrivalRate1=np.matmul(retailerArrivalRate1,np.array(X))
        retailerArrivalRate2=np.reshape(self.RETAILER_ARRIVAL_RATE_2,(1,self.NO_OF_RETAILER))
        dcArrivalRate2=np.matmul(retailerArrivalRate2,np.array(X))
        DC_ARRIVAL_RATE_1=[ar for _,ar in enumerate(dcArrivalRate1)]
        DC_ARRIVAL_RATE_2=[ar for _,ar in enumerate(dcArrivalRate2)]
        return DC_ARRIVAL_RATE_1,DC_ARRIVAL_RATE_2

    def generateX(self,chromosome:list):
        '''Matrix X is generated for each chromosome'''
        X=np.zeros((self.NO_OF_RETAILER,self.NO_OF_DC)).astype(int)
        for idx,dc in enumerate(chromosome):
            X[idx][dc-1]=1
        return X
      
    def generateY(self,X):
        '''Matrix Y is generated based on X'''
        Y=np.zeros(self.NO_OF_DC).astype(int).tolist()
        for j in range(self.NO_OF_DC):
        #Loop each retailer whether it got assign to the DC 
            for i in range(self.NO_OF_RETAILER):
                if (X[i][j]==1):
                    Y[j]=1 
        return Y
      
    def calcTerm1(self,Y:list):
        '''Term 1: Calculate fixed cost of each DC'''  
        fixedCost=0
        for j in range(self.NO_OF_DC):
            fixedCost+=self.FIXED_COST[j]*Y[j]
        return fixedCost
    
    def calcProbState0(self,s:list,Q:list):
        '''Calculate probability at Stage 0'''
        probState0List=[]
        for j in range(self.NO_OF_DC):
            probState0List.append(self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j])/(self.DC_ARRIVAL_RATE_1[j]+(self.DC_ARRIVAL_RATE_2[j]+(Q[j]*self.LEAD_TIME[j]))*pow((1+self.LEAD_TIME[j]/self.DC_ARRIVAL_RATE_1[j]),s[j]))
        return probState0List
    
    def calcInventoryLevelCost(self,s:list,Q:list):#TODO
        '''Calculate inventory level cost for each DC'''
        ilCostList=[]
        self.probState0List=self.calcProbState0(s,Q)
        for j in range(self.NO_OF_DC):
            a=pow((1+self.LEAD_TIME[j]/self.DC_ARRIVAL_RATE_1[j]),s[j])
            b=(s[j]*self.DC_ARRIVAL_RATE_2[j])/(self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j])
            c=(self.LEAD_TIME[j]*Q[j]*(Q[j]+2*s[j]+1))/(2*self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j])
            d=(Q[j]*self.DC_ARRIVAL_RATE_1[j])/(self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j])
            e=(self.DC_ARRIVAL_RATE_1[j]*self.DC_ARRIVAL_RATE_2[j])/(self.LEAD_TIME[j]*(self.DC_ARRIVAL_RATE_1[j]*self.DC_ARRIVAL_RATE_2[j]))
            f=Q[j]+(self.DC_ARRIVAL_RATE_2[j]/self.LEAD_TIME[j])
            g=(self.DC_ARRIVAL_RATE_1[j]/(self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j]))
            ilCostList.append(a*((b+c-d-e)*self.probState0List[j])+f*g*self.probState0List[j])
        return ilCostList

    def calcTerm2(self,Y:list,s:list,Q:list):
        '''Term 2: Calculate holding cost of each DC'''
        totalHoldingCost=0
        self.il=self.calcInventoryLevelCost(s,Q) 
        for j in range(self.NO_OF_DC):
            totalHoldingCost+=self.HOLDING_COST[j]*(self.il[j])*Y[j]
        return totalHoldingCost
        
    def calcReorderRate(self,s:list,Q:list):
        reorderCostList=[]
        probState0=self.calcProbState0(s,Q)
        for j in range(self.NO_OF_DC):
            reorderCostList.append(self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j])*probState0[j]*(s[j]+1)
        return reorderCostList

    def calcTerm3(self,Y:list,Q:list):
        '''Term 3: Calculate setup cost, unit purchasing cost and fixed shipping cost per order between Supplier and DC'''
        total=0
        self.reorderCostList=self.calcReorderRate
        for j in range(self.NO_OF_DC):
            # Q_MIN_OF_J, REORDERRATE !
            total+=(self.SETUP_COST[j]+self.FIXED_SHIPPING_COST[j]+(self.PURCHASING_COST_UNIT[j]*(Q[j])))*(self.reorderCostList[j])*Y[j]
        return total

    def calcTerm4(self,X:list):
        '''Term 4: Transportation cost from DC to the retailer'''
        total=0
        for j in range(self.NO_OF_DC):
            for i in range(self.NO_OF_RETAILER):
                for r in range(len(self.CUSTOMER_CLASS.keys())):
                    if(r==0):#Calculate priority arrival rate
                        #MUST ENSURE ARRIVAL RATE IS FOR RETAILER NOT DC
                        #DOUBLE CHECK SHIPPING COST IS MATRIX, MAKE SURE ROW N COL IS COLUMN
                        total+=self.RETAILER_ARRIVAL_RATE_1[i]*self.SHIPPING_COST[i][j]*X[i][j]
                    else: #Calculate ordinary arrival rate
                        total+=self.RETAILER_ARRIVAL_RATE_2[i]*self.SHIPPING_COST[i][j]*X[i][j]
        return total

    def calcShortageRate1(self):
        '''Calculate Mean Shortage Rates for the PRIORITY customers at each DC'''
        shortageRate1List=[]
        for j in range(self.NO_OF_DC):
            shortageRate1List.append(self.DC_ARRIVAL_RATE_1[j]*self.probState0List[j])
        return shortageRate1List 

    def calcShortageRate2(self,s):
        '''Calculate Mean Shortage Rates for the ORDINARY customers at each DC'''
        shortageRate2List=[]
        for j in range(self.NO_OF_DC):
            shortageRate2List.append(self.DC_ARRIVAL_RATE_2[j]*pow((1+self.LEAD_TIME[j]/self.DC_ARRIVAL_RATE_1[j]),s[j])*self.probState0List[j])
        return shortageRate2List

    def calcTerm5(self,Y:list):
        totalLostCost=0
        self.meanShortageRate1=self.calcShortageRate1()
        self.meanShortageRate2=self.calcShortageRate2()
        for j in range(self.NO_OF_DC):
            for r in range(len(self.CUSTOMER_CLASS.keys())): 
                if (r==0): #MSR for priority customer
                    totalLostCost+=self.meanShortageRate1[j]*self.COST_LOSE_1*Y[j] 
                else: #MSR for ordinary customer
                    totalLostCost+=self.meanShortageRate2[j]*self.COST_LOSE_2*Y[j] 
        return totalLostCost

    def penaltyCost(self,chromosome):
        '''Calculate penalty cost for dummy DC'''
        #Cal how many customers assign to DC then multiply (1 penalty add 10k)
        #Got how many retailers assign to that DC
        #Count total dummy DC in chromosomes there (Loop chromosome)
        totalPenaltyCost=0
        #dummyDCCount=[if gene==1  for idx,gene in enumerate(chromosome)]
        dummyDCCount=chromosome.count(self.NO_OF_DC+1)
        for i in range(self.NO_OF_RETAILER):
            if chromosome[i]==self.NO_OF_DC+1: #If that current gene is the DUMMY DC, then add penalty cost
                totalPenaltyCost+=10000
        return totalPenaltyCost
    
    def calcTotalCost(self,X:list,Y:list,s,Q):
        '''Calculate min total cost (TC)'''
        return self.calcTerm1(Y)+self.calcTerm2(Y,s,Q)+self.calcTerm3()+self.calcTerm4()+self.calcTerm5()
    
    #TODO Try to do total cost for one DC, no need to loop j
    def calcTotalCostForEachDC(self,X:list,Y,s,Q,j): #X is matrix, only pass that column(ONLY COL), Y only 1 or 0 not list d
        pass

    def calcQmin(self):
        '''Step 1: Calculate Qmin for each DC'''
        Qmin=[]
        for j in range(self.NO_OF_DC):
            QminCost=((self.COST_LOSE_1-self.PURCHASING_COST_UNIT[j])*self.DC_ARRIVAL_RATE_1[j]*(self.DC_ARRIVAL_RATE_1[j]+self.DC_ARRIVAL_RATE_2[j]))/(self.HOLDING_COST[j]*self.LEAD_TIME[j])
            Qmin.append(QminCost) 
        return Qmin
    
#Create SC instance objects
def main():
    sc_small_II=SupplyChain('5-10','TYPE_II')
main()
