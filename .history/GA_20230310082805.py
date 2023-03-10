from SupplyChain import SupplyChain 
import random
import numpy as np

class GA:
    random.seed(42)
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc:SupplyChain):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        self.sc=sc
        self.INDIVIDUAL_LENGTH=self.sc.NO_OF_RETAILER
        #TODO rmb to change back NO_OF_RETAILER & DC

    #=======================================================================================================
    def generateChromosome(self):
        '''Generating chromosomes based on the size of DC and retailer'''
        #NO_OF_DC+1 cater for the dummy DC
        chromosome=[random.randint(1,sc.NO_OF_DC+1) for i in range(sc.NO_OF_RETAILER)]
        return chromosome
        
    #=======================================================================================================
    def evaluateChromosome(self,chromosome): 
        '''Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #Generate X and Y
        X=self.sc.generateX(chromosome)
        Y=self.sc.generateY(X)
        #Compute optimum s and Q (a list with j elements) 
        finalOptimalSQ=self.calcOptimumSQ(X,Y)
        #Then pass to fitness:  #TODO check X or Y whether dummy DC is got open or not, if got add penalty cost
        fitness=self.sc.calcPenaltyCost(chromosome)+self.sc.calcTotalCost()
        return fitness

    #=======================================================================================================
    def elitism(self):
        '''Retaining the best individuals in a gen unchanged in the next gen'''
        pass

    #=======================================================================================================
    def rouletteWheelSelection(self):
        '''Parents selection based on roulette wheel selection'''
        pass

    #=======================================================================================================
    def crossOver(self,n_parents):
        '''Crossover 2 parents to generate new offspring'''
        pass
    #=======================================================================================================
    def inversion_mutation(population,chromosome):
        '''Mutation used to maintain the genetic diversity of the chromosomes'''
        #     #Mutation operator in GA avoids convergence to local optimum and diverfies the population
        #     #Replacing a gene with a randomly selected number according to the parameter's boundaries
        pass

    #=======================================================================================================
    def evaluateOffsprings(self):
        '''Evaluate the performance of offsprings'''
        #Best chromosome, everytime will check whether it will better than best chromosome
        pass

    #=======================================================================================================
    def calcOptimumSQ(self,X,Y):
        '''Find optimal S0j, Q0j and costs'''
        #-- Step1: Find Qmin for each DC --
        Qmin=self.sc.calcQmin()

        #-- Step 2:Calculate Q0 and s0 to find optimal Q0 and s0 --
        #Loop for every DC's s0 and q0
        s0List=[] 
        q0List=[]
        for j in range(self.sc.NO_OF_DC):#Loop every DC to calculate
            breakQFlag=False #If found correct then break
            minValue=9999 #In case cannot found=0, then found the nearest min value
            targetS0=None 
            targetQ0=None
            for q0 in reversed(range(2,round(Qmin[j]))): #Loop q0, starting from q1-1 reversed=1259
                #For every q0 test for every s0
                for s0 in range(1,q0):#X only take one column try 1-1258
                    diff=self.sc.calcTotalCostForEachDC(X[j],Y[j],s0+1,q0)-self.sc.calcTotalCostForEachDC(X[j],Y[j],s0,q0)
                    if diff<minValue:
                        minValue=diff
                        targetS0=s0
                        targetQ0=q0
                    elif diff==0:
                        minValue=0
                        s0List.append(s0)
                        q0List.append(q0)
                        breakQFlag=True
                        break
                if breakQFlag==True:
                    break
            #If cannot cater 0
            if minValue!=0:
                s0List.append(targetS0)
                q0List.append(targetQ0)

        #-- Step 3: Find optimal Q1j when s=0 --
        q1List=[]
        for j in range(self.sc.NO_OF_DC):
            breakQFlag=False
            minValue=9999 
            targetQ1=None
            for q1 in range(1,round(Qmin[j])):
                diff=self.sc.calcTotalCostForEachDC(X[j],Y[j],0,q1+1)-self.sc.calcTotalCostForEachDC(X[j],Y[j],0,q1)
                if diff<minValue:
                    minValue=diff
                    targetQ1=q1
                elif diff==0:
                    minValue=0
                    q1List.append(q1)
                    breakQFlag=True
                    break
                if breakQFlag==True:
                    break
            #If cannot cater 0
            if minValue!=0:
                q1List.append(targetQ1)
        
        #-- Step 4: Compare the TC cost based on Step 2 and 3, find the optimal s and q --
        finalOptimalSQ=[]
        for j in range(self.sc.NO_OF_DC):
            tcCost1=self.sc.calcTotalCostForEachDC(X[j],Y[j],s0List[j],q0List[j])
            tcCost2=self.sc.calcTotalCostForEachDC(X[j],Y[j],0,q1List[j])
            if(tcCost1<tcCost2):
                #Save as tuple
                finalOptimalSQ.append((s0List[j],q0List[j]))
            else:#tcCost1>tcCost2
                finalOptimalSQ.append((0,q1List[j]))

        return finalOptimalSQ
           
    def run(self):
        '''Function to run the GA'''
        #Step 1: Initiating first population
        self.population=[self.generateChromosome() for _ in range(self.POP_SIZE)]
        
        for iter in range(self.MAX_GENERATION): #Total iterations
            #Step 2: Evaluating chromosome
            ranked_population=[]
            for idx,chromosome in enumerate(self.population):
                ranked_population.append(self.evaluateChromosome(chromosome))
            
            #Step 3: Reproduction (Elitism)

            #Step 4: Parents selection

            #Step 5: Crossover

            #Step 6: 
            pass
        
        

sc=SupplyChain('5-10','TYPE_I')
MAX_GENERATION=10000
POP_SIZE=20
MAX_SAME_ANSWER_PRODUCED=100
CROSS_RATE=0.8
GEN_MUT_RATE=0.2
GA=GA(MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc)
GA.run()


