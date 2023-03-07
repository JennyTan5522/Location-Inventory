import yaml
import random

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

        #GA Goal: DC want open or not, which retailer under which DC
        #Create a cost list, assign a random value based on the cost range of SITUATION_TYPE for each DC
        self.SETUP_COST=[random.randint(cost_list['SETUP_COST'][0],cost_list['SETUP_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.HOLDING_COST=[random.randint(cost_list['HOLDING_COST'][0],cost_list['HOLDING_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.PURCHASING_COST_UNIT=[random.randint(cost_list['PURCHASING_COST_UNIT'][0],cost_list['PURCHASING_COST_UNIT'][1]) for _ in range(self.NO_OF_DC)]
        self.SHIPPING_COST=[random.randint(cost_list['SHIPPING_COST'][0],cost_list['SHIPPING_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.LEAD_TIME=[random.randint(cost_list['LEAD_TIME'][0],cost_list['LEAD_TIME'][1]) for _ in range(self.NO_OF_DC)]
        self.FIXED_SHIPPING_COST=[random.randint(cost_list['FIXED_SHIPPING_COST'][0],cost_list['FIXED_SHIPPING_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.ARRIVAL_RATE=[random.randint(cost_list['ARRIVAL_RATE'][0],cost_list['ARRIVAL_RATE'][1]) for _ in range(self.NO_OF_DC)]
        self.FIXED_COST=[random.randint(cost_list['FIXED_COST'][0],cost_list['FIXED_COST'][1]) for _ in range(self.NO_OF_DC)]
        self.COST_LOSE_1=cost_list['COST_LOSE_P']
        self.COST_LOSE_2=cost_list['COST_LOSE_O']
        self.CUSTOMER_CLASS={'1':'Priority','2':'Ordinary'}
     
        print('Number of suppliers : ',self.NO_OF_SUPPLIER)
        print('Number of DCs       : ',self.NO_OF_DC)
        print('Number of retailers : ',self.NO_OF_RETAILER)
        print('                   Costs Listing')
        print('=============================================================')
        print('Setup cost      : ',self.SETUP_COST)
        print('Holding cost    : ',self.HOLDING_COST)
        print('Purchasing cost : ',self.HOLDING_COST)
        print('Shipping cost   : ',self.SHIPPING_COST)
        print('Lead time       : ',self.LEAD_TIME)
        print('Shipping cost   : ',self.FIXED_SHIPPING_COST)
        print('Arrival rate    : ',self.ARRIVAL_RATE)
        print('Fixed cost      : ',self.FIXED_COST)
        print('Cost losing priority customer : ',self.COST_LOSE_1)
        print('Cost losing ordinary customer : ',self.COST_LOSE_2)
      
    
    def calcTotalCost(self,X,Y,s,Q):
        return self.calcTerm1(Y)+self.calcTerm2(Y,s,Q)+self.calcTerm3()+self.calcTerm4()+self.calcTerm5()
    
    def calcTerm1(self,Y:list):
        '''Term 1: Calculate fixed cost of each DC'''  
        totalFixedCost=0
        for j in range(self.NO_OF_DC):
            totalFixedCost+=self.FIXED_COST[j]*Y[j]
        return totalFixedCost
    
    def calcInventoryLevelCost(self,s,Q):#TODO
        pass

    def calcTerm2(self,Y:list,s,Q):
        '''Term 2: Calculate holding cost of each DC'''
        totalHoldingCost=0
        self.il=self.calcInventoryLevelCost(s,Q) #If s and Q are list TODO
        for j in range(self.NO_OF_DC):
            totalHoldingCost+=self.HOLDING_COST[j]*(il[j])*Y[j]
        return totalHoldingCost
    
    def calcProbState0(self,s,Q):
        '''Calculate probability at Stage 0'''
        #return Pj (list: for every j got their values)
        pass

    def calcReorderRate(self,s):
        pass

    def calcTerm3(self,Y:list,Q):
        '''Term 3: Calculate setup cost, unit purchasing cost and fixed shipping cost per order between Supplier and DC'''
        total=0
        for j in range(self.NO_OF_DC):
            # Q_MIN_OF_J, REORDERRATE !
            total+=(self.SETUP_COST[j]+self.FIXED_SHIPPING_COST[j]+(self.PURCHASING_COST_UNIT[j]*(Q[j])))*(self.calcReorderRate)*Y[j]
        return total

    def calcTerm4(self,X):
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

    #In list
    def calcShortageRate1(self):
        pass

    def calcShortageRate2(self,s):
        pass

    def calcTerm5(self):
        totalLostCost=0
        #Calculate shortage rate,call for 
        meanShortageRate1=self.calcShortageRate1()
        meanShortageRate2=self.calcShortageRate2()

        for j in range(NO_OF_DC):
            for r in range(CUSTOMER_CLASS): #CUSTOMER CLASS !
                totalLostCost+=self.MEAN_SHORTAGE_RATE[j]*COST_LOSE_[r]*Y[j] #MEAN_SHORTAGE_RATE !
    


    
                
    


        
#Create SC instance objects
def main():
    sc_small_II=SupplyChain('5-10','TYPE_II')
main()
