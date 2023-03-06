import yaml
import re
import random

random.seed(42)

class SupplyChain:
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
        COST_LOSE_P=cost_list['COST_LOSE_P']
        COST_LOSE_O=cost_list['COST_LOSE_O']
     
        print('Number of suppliers: ',self.NO_OF_SUPPLIER)
        print(self.NO_OF_SUPPLIER,self.NO_OF_DC,self.NO_OF_RETAILER)
        print(self.SETUP_COST,self.HOLDING_COST,self.PURCHASING_COST_UNIT,self.SHIPPING_COST)
        # print(self.LEAD_TIME,self.FIXED_SHIPPING_COST,self.ARRIVAL_RATE)
        # print(self.FIXED_COST,self.COST_LOSE_P,self.COST_LOSE_O)
    
    def generateChromosome(self):
        chromosome=[[random.randint(1,self.NO_OF_DC) for i in range(self.NO_OF_RETAILER)]  for j in range(self.NO_OF_DC)]

        
#Create SC instance objects
def main():
    sc_small_I=SupplyChain('5-10','TYPE_II')
main()
