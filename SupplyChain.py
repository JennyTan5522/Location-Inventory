import yaml
import random
import numpy as np

class SupplyChain:
    
    def __init__(self,PROBLEM_SIZE,SITUATION_TYPE,display_param=False):
        random.seed(42)

        #Load yaml file
        with open('PARAMETERS_INITIALIZATION.yml','r') as f:
            PARAMETERS_INITIALIZATION=yaml.safe_load(f)

        #Find problem size and initialize each number of Suppliers, DCs and Retailers
        try:
            number_probSize = PARAMETERS_INITIALIZATION['PROBLEM_SIZE'][PROBLEM_SIZE]
        except:
            raise ValueError(f"Unknown Problem Size - {PROBLEM_SIZE}")
    
        #Find cost based on situation type
        try:
            cost_list = PARAMETERS_INITIALIZATION['SITUATION_TYPE'][SITUATION_TYPE]
        except:
            raise ValueError(f"Unknown Situation Type - {SITUATION_TYPE}")
        
        #Problem size initialization          
        self.NO_OF_SUPPLIER, self.NO_OF_DC, self.NO_OF_RETAILER = number_probSize

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

        if display_param:
            self.display_param()

    def display_param(self):
        """Display parameters initialized."""
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
        print('Retailer arrival rate priority   : ',self.RETAILER_ARRIVAL_RATE_1)
        print('Retailer arrival rate ordinary   : ',self.RETAILER_ARRIVAL_RATE_2)
        print('Fixed cost      : ',self.FIXED_COST)
        print('Cost losing priority customer : ',self.COST_LOSE_1)
        print('Cost losing ordinary customer : ',self.COST_LOSE_2)

    def calcDcArrivalRate(self, X:list):
        '''Find DC arrival rate based on retailer arrival rate. Arrival rate depends on X.
           Execute this function after compute X. Call from GA.py
        '''
        # Chromosome -> X -> generate DC Arrival rate -> Compute total cost
        retailerArrivalRate1 = np.reshape(self.RETAILER_ARRIVAL_RATE_1,(1,self.NO_OF_RETAILER))
        dcArrivalRate1 = np.matmul(retailerArrivalRate1,np.array(X))
        self.DC_ARRIVAL_RATE_1 = [ar for _,ar in enumerate(dcArrivalRate1)]
        
        retailerArrivalRate2 = np.reshape(self.RETAILER_ARRIVAL_RATE_2,(1,self.NO_OF_RETAILER))
        dcArrivalRate2 = np.matmul(retailerArrivalRate2,np.array(X))
        self.DC_ARRIVAL_RATE_2 = [ar for _,ar in enumerate(dcArrivalRate2)]
        
    def calcProbState0(self,s:list,Q:list):
        '''Calculate probability at Stage 0 - each dc has its own probstate0'''
        return np.divide(np.add(self.DC_ARRIVAL_RATE_1,self.DC_ARRIVAL_RATE_2),
                         np.add(self.DC_ARRIVAL_RATE_1, 
                                np.multiply(np.add(self.DC_ARRIVAL_RATE_2,np.multiply(Q,self.LEAD_TIME)),
                                            np.power(np.add(1,np.divide(self.LEAD_TIME, self.DC_ARRIVAL_RATE_1)),s))))
    
    def calcInventoryLevelCost(self,s:list,Q:list):
        '''Calculate inventory level cost for each DC - each dc has its own IL'''
        t1 = np.power(np.add(1, np.divide(self.LEAD_TIME, self.DC_ARRIVAL_RATE_1)), s)
        
        t2a = np.divide(np.multiply(s, self.DC_ARRIVAL_RATE_2), self.add(self.DC_ARRIVAL_RATE_1,self.DC_ARRIVAL_RATE_2))
        t2b = np.divide(np.multiply(np.multiply(self.LEAD_TIME, Q), np.add(np.add(Q, np.multiply(2,s)),1)),
                        np.multiply(2, np.add(self.DC_ARRIVAL_RATE_1, self.DC_ARRIVAL_RATE_2)))
        t2c = np.divide(np.multiply(Q, self.DC_ARRIVAL_RATE_1), np.add(self.DC_ARRIVAL_RATE_1, self.DC_ARRIVAL_RATE_2))
        t2d = np.divide(np.multiply(self.DC_ARRIVAL_RATE_1, self.DC_ARRIVAL_RATE_2), 
                        np.multiply(self.LEAD_TIME, np.add(self.DC_ARRIVAL_RATE_1, self.DC_ARRIVAL_RATE_2)))
        t2 = np.multiply(np.subtract(np.subtract(np.add(t2a, t2b), t2c), t2d), self.probState0List)
        
        t3a = np.add(Q, np.divide(self.DC_ARRIVAL_RATE_2, self.LEAD_TIME))
        t3b = np.divide(self.DC_ARRIVAL_RATE_1, np.add(self.DC_ARRIVAL_RATE_1, self.DC_ARRIVAL_RATE_2))
        t3 = np.multiply(np.multiply(t3a, t3b), self.probState0List)
        
        return np.add(np.multiply(t1, t2), t3)

    def calcReorderRate(self,s:list):
        '''Compute mean reorder rate, R for each j'''
        return np.multiply(np.multiply(self.LEAD_TIME, 
                                       np.power(np.add(1, np.divide(self.LEAD_TIME, self.DC_ARRIVAL_RATE_1)), s)), 
                           self.probState0List)

    def calcShortageRate1(self):
        '''Calculate Mean Shortage Rates for the PRIORITY customers at each DC'''
        return np.multiply(self.DC_ARRIVAL_RATE_1, self.probState0List)

    def calcShortageRate2(self,s):
        '''Calculate Mean Shortage Rates for the ORDINARY customers at each DC'''
        return np.multiply(np.multiply(self.DC_ARRIVAL_RATE_2,
                                       np.power(np.add(1, np.divide(self.LEAD_TIME, self.DC_ARRIVAL_RATE_1)), s)),
                           self.probState0List)
    
    def calcTerm1(self,Y:list):
        '''Term 1: Calculate fixed cost of each DC
            f[j] * Y[j]
        '''  
        return np.dot(self.FIXED_COST, Y)
    
    def calcTerm2(self,Y:list):
        '''Term 2: Calculate holding cost of each DC
            h[j] * IL[j] * Y[j]
        '''
        return (np.dot(np.multiply(self.HOLDING_COST,self.il),Y))
        
    def calcTerm3(self,Y:list,Q:list):
        '''Term 3: Calculate setup cost, unit purchasing cost and fixed shipping cost per order between Supplier and DC
            (k[j] + g[j] + c[j] * Q[j]) * R[j] * Y[j]       
        '''
        return np.dot(np.multiply(np.add(np.add(self.SETUP_COST,self.FIXED_SHIPPING_COST),
                                         np.multiply(self.PURCHASING_COST_UNIT,Q)),
                                  self.reorderCostList),Y)

    def calcTerm4(self,X:list):
        '''Term 4: Transportation cost from DC to the retailer
            lambda[r][i] * C[i][j] * X[i][j]
        '''
        return np.sum(np.add(np.dot(self.RETAILER_ARRIVAL_RATE_1, np.multiply(self.SHIPPING_COST,X)),
                             np.dot(self.RETAILER_ARRIVAL_RATE_2, np.multiply(self.SHIPPING_COST,X))))        

    def calcTerm5(self,Y:list):
        '''Term 5: lost sales due to demand lost for each customer classes
            SR[r][j] * LC[r] * Y[j]
        '''
        return np.dot(np.multiply(self.meanShortageRate1,self.COST_LOSE_1),Y) + \
               np.dot(np.multiply(self.meanShortageRate2,self.COST_LOSE_2),Y)

    def penaltyCost(self,chromosome:list):
        '''Calculate penalty cost for dummy DC'''
        #Calc penalty cost based on how many retailer assign to dummy DC
        return chromosome.count(self.NO_OF_DC+1)*10000
    
    #TODO check X or Y whether dummy DC is got open or not, if got add penalty cost
    def calcTotalCost(self,X:list,Y:list,s:list,Q:list,targetDC=None):
        '''Calculate total cost (TC) givem X, Y, s & Q
            :targetDC: assign the DC ID only if want to compute the total cost for that particular DC
        '''

        # Compute param that affected by X, s & q - required to update once hv new s & q
        self.probState0List = self.calcProbState0(s,Q)
        self.il = self.calcInventoryLevelCost(s,Q)
        self.reorderCostList = self.calcReorderRate(s)
        self.meanShortageRate1 = self.calcShortageRate1()   # only able to compute after computing probState0List
        self.meanShortageRate2 = self.calcShortageRate2(s)
        
        if targetDC is not None:
            """
            When computing TC, the cost incurred by DC will only be calculated if the DC is open.
            To calc TC for a particular DC, assign 0 for all the other DC in X and Y.
            For example: targetDC = 2
                         X = [[1,0,1,0,1], --> [[0,0,0,0,0],
                              [0,1,0,1,0]]      [0,1,0,0,0]]
                         Y = [1,1,0,1,1] --> [0,1,0,0,0]   
            """
            X = [[elem if idx==(targetDC-1) else 0 for idx, elem in enumerate(X[i])] for i in range(len(X))]
            Y = [elem if idx==(targetDC-1) else 0 for idx, elem in enumerate(Y)]

        return self.calcTerm1(Y) + \
               self.calcTerm2(Y) + \
               self.calcTerm3(Y,Q) + \
               self.calcTerm4(X) + \
               self.calcTerm5(Y)

    def calcQmin(self):
        '''Step 1: Calculate Qmin for each DC
            return list of Qmin with size j
        '''
        return np.divide(np.multiply(np.multiply(np.subtract(self.COST_LOSE_1, self.PURCHASING_COST_UNIT),
                                                 self.DC_ARRIVAL_RATE_1),
                                     np.add(self.DC_ARRIVAL_RATE_1+self.DC_ARRIVAL_RATE_2)),
                         np.multiply(self.HOLDING_COST, self.LEAD_TIME))
    
#Create SC instance objects
if __name__ == "__main__":
    sc_small_II = SupplyChain('5-10','TYPE_II', display_param=True)


