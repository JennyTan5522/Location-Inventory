from SupplyChain import SupplyChain 
import random
import numpy as np
import math

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

    def generateChromosome(self):
        '''Generating chromosomes based on the size of DC and retailer'''
        #NO_OF_DC+1 cater for the dummy DC
        chromosome=[random.randint(1,sc.NO_OF_DC+1) for i in range(sc.NO_OF_RETAILER)]
        return chromosome
    
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
        
    def evaluateChromosome(self,chromosome): 
        '''Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #Generate X and Y
        X=self.sc.generateX(chromosome)
        Y=self.sc.generateY(X)
        #Compute optimum s and Q (a list with j elements) 
        finalOptimalSQ=self.calcOptimumSQ(X,Y)
        #Check constraint, if not fulfill

        #Then pass to fitness:  #TODO check X or Y whether dummy DC is got open or not, if got add penalty cost
        fitness=self.sc.calcPenaltyCost(chromosome)+self.sc.calcTotalCost()
        return fitness

    def rouletteWheelSelection(self,population):
        population_fitness=sum([self.evaluateChromosome(population[ind]) for ind in range(len(population))])
        #Compute each chromosome's probability 
        chromosome_prob=[self.evaluateChromosome(chromosome)/population_fitness for chromosome in population]
        #Making the prob for minimization prob
        chromosome_prob=1-np.array(chromosome_prob)
        chromosome_prob=chromosome_prob.tolist()
        #Generate random r, if a current sum>r, then select that chromosome
        return population[chromosome_prob.index(np.random.choice(chromosome_prob))]

    def cross_over(self,parent1,parent2):
        #Get the random number to split and perform crossover
        pos=random.randrange(1,len(parent1)-1)
        child1=parent1[:pos]+parent2[pos:]
        child2=parent2[:pos]+parent1[pos:]
        return child1,child2

    def mutation(self,chromosome):
        #Generate a random number based on the range of NO_OF_DC, then iterate based on the mutation iteration
        mutation_no=random.randint(1,self.sc.NO_OF_DC)
        #Replace chromosome index with mutation no
        replace_index=random.randint(0,self.INDIVIDUAL_LENGTH-1)
        chromosome[replace_index]=mutation_no
        return chromosome
    
    def newGeneration(self):
        history={}
        best_individual=(9999999,0)
        #Step 1: Initiating first population
        self.population=[self.generateChromosome() for _ in range(self.POP_SIZE)]

        for iter in range(self.MAX_GENERATION):
            ranked_population=[]
            #Step 2: Evaluating chromosome
            for chromosome in enumerate(population):
                ranked_population.append((self.evaluateChromosome(chromosome[1]),chromosome[1]))

            #Rank from low to high -> The lowest the better
            ranked_population.sort()

            #Compare the current population's best individual with the current best individual
            if(ranked_population[0][0]<best_individual[0]):
                best_individual=ranked_population[0]
                
            #Update history
            history[iter]={'Best':ranked_population[0][0]}

            #Step 3: Elitism - Select the top 20% from ranked_pop which use to remain for next generation
            elitism_population=[ind[1] for ind in ranked_population[:round(POP_SIZE*0.2)]]

            #Parent selection and crossover
            n_parents=round(POP_SIZE*0.8)
            #Make sure n_parents is in an even number
            n_parents=(n_parents if n_parents%2==0 else n_parents-1)
            new_population=[]
            for i in range(0,n_parents,2):
                if random.uniform(0,1)<CROSS_RATE:
                    while(True):
                        #Step 4: Parent selection - Select 80% from ranked_pop for parent selection
                        parent1=self.rouletteWheelSelection(population)
                        parent2=self.rouletteWheelSelection(population)
                        if parent1!=parent2:
                            break
                    #Step 5: Crossover
                    child1,child2=self.cross_over(parent1,parent2)
                    new_population.append(child1)
                    new_population.append(child2)
                else:
                    new_population.append(population[i])
                    new_population.append(population[i+1])

            #Step 6: Mutation - Undergo mutation process if the random generated no < 0.2
            for idx,ind in enumerate(new_population):
                #10% of genes from selected chromosomes for crossover are chosen
                if random.uniform(0,1) < GEN_MUT_RATE:
                    mut_iter=math.ceil(self.INDIVIDUAL_LENGTH*0.1)
                    for i in range(mut_iter):
                        new_population[idx]=self.mutation(ind)

            population=elitism_population+new_population

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
        #finalOptimalSQ=[]
        optimalS=[]
        optimalQ=[]
        for j in range(self.sc.NO_OF_DC):
            tcCost1=self.sc.calcTotalCostForEachDC(X[j],Y[j],s0List[j],q0List[j])
            tcCost2=self.sc.calcTotalCostForEachDC(X[j],Y[j],0,q1List[j])
            if(tcCost1<tcCost2):
                #Save as tuple
                optimalS.append(s0List[j])
                optimalQ.append(q0List[j])
            else:#tcCost1>tcCost2
                optimalS.append(s0List[j])
                optimalQ.append(q0List[j])
        
sc=SupplyChain('5-10','TYPE_I')
MAX_GENERATION=10000
POP_SIZE=20
MAX_SAME_ANSWER_PRODUCED=100
CROSS_RATE=0.8
GEN_MUT_RATE=0.2
GA=GA(MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc)
GA.newGeneration()


