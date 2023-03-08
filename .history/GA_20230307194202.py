from SupplyChain import SupplyChain
import random
from random import sample
import numpy as np

class Genetic_Algorithm():
    #random.seed(42)
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        self.sc=sc
        self.INDIVIDUAL_LENGTH=sc.NO_OF_RETAILER
        #TODO rmb to change back NO_OF_RETAILER & DC

    #=======================================================================================================
    def initialPopulation(self):
        '''Step 1: Initiating first population'''
        #TODO inside need self
        def generateX(chromosome):
            '''Matrix X is generated for each chromosome'''
            X=np.zeros((sc.NO_OF_RETAILER,sc.NO_OF_DC)).astype(int)
            for idx,dc in enumerate(chromosome):
                X[idx][dc-1]=1
            return X
        
        def generateY(X):
            '''Matrix Y is generated based on X'''
            Y=np.zeros(sc.NO_OF_DC).astype(int).tolist()
            for j in range(sc.NO_OF_DC):
            #Loop each retailer whether it got assign to the DC 
                for i in range(sc.NO_OF_RETAILER):
                    if (X[i][j]==1):
                        Y[j]=1 
            return Y

        def generateChromosome():
            '''Generating chromosomes based on population size'''
            chromosome=[random.randint(1,sc.NO_OF_DC) for i in range(sc.NO_OF_RETAILER)]
            return chromosome
        
        #TODO i just return population will do
        
    #=======================================================================================================
    def evaluateChromosome(self):
        '''Step 2: Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #self.sc.calcTotalCost(X,Y,s,Q)
        pass

    #=======================================================================================================
    def elitism(self):
        '''Step 3: Retaining the best individuals in a gen unchanged in the next gen'''
        pass

    #=======================================================================================================
    def new_generation(self):
        '''Step 4: Parents selection based on roulette wheel selection'''
        def rouletteWheelSelection(population):
            fitness=0 #TODO replace to fitness value
            #1. Random selection of 80% chromosomes from population
            chromosomesSample=sample(population,round(len(population)*0.8))
            #Calculate cumulative sum of fitness from 80% selected chromosomes
            cumulativeSum=np.cumsum(population) #TODO population change to 'fitness'
            #Generate a random number between 0 and cumulativeSum, choose the individual with cumulativeSum < fitness
            random=cumulativeSum*np.random.rand()
            index=np.argwhere(random<=cumulativeSum)
            return index[0][0]
        #=======================================================================================================
        def crossOver(n_parents):
            '''Step 5: Crossover 2 parents to generate new offspring'''
            childs=[]
            #Select 2 parents and pass to crossOverParent
            for i in range(0,len(n_parents),2):
                pos=random.randint(1,self.INDIVIDUAL_LENGTH-1)
                child1=n_parents[i][:pos]+n_parents[i+1][pos:]
                child2=n_parents[i+1][:pos]+n_parents[i][pos:]
                childs.append(child1,child2)
            return childs
            #3. Ensure that the parents selected are not duplicated TODO
            
        #=======================================================================================================
        # def inversion_mutation(population,chromosome):
        #     '''Step 6: Mutation used to maintain the genetic diversity of the chromosomes'''
        #     #Mutation operator in GA avoids convergence to local optimum and diverfies the population
        #     #Replacing a gene with a randomly selected number according to the parameter's boundaries
        #     for i in population:
        #         for _ in range(len(self.INDIVIDUAL_LENGTH)):
        #             if random.random()<self.GEN_MUT_RATE:
        #                 idx1=random.randint(0,self.INDIVIDUAL_LENGTH-1)
        #                 idx2=random.randint(idx1,self.INDIVIDUAL_LENGTH-1)
        #                 chromosome_mid=chromosome[idx1:idx2]
        #                 chromosome_mid.reverse()
        #                 chromosome_result=chromosome[0:idx1]+chromosome[idx2:]
        #             return chromosome_result
            
        
        # crosses=crossOver()
        # mutations=mutation()

    #=======================================================================================================
    def evaluateOffsprings(self):
        '''Step 7: Evaluate the performance of offsprings'''
        pass

    #=======================================================================================================
    Genetic_Algorithm=initialPopulation()

sc=SupplyChain('5-10','TYPE_I')
MAX_GENERATION=10000
POP_SIZE=20
MAX_SAME_ANSWER_PRODUCED=100
CROSS_RATE=0.8
GEN_MUT_RATE=0.2
GA=Genetic_Algorithm(MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc)
# population=[GA.generateChromosome() for _ in range(POP_SIZE)]
# X=[GA.generateX(population[idx]) for idx in range(len(population))]
# Y=[GA.generateY(X[idx]) for idx in range(len(population))]    
# print(population)  
# print(X)
# print(Y)  
# #2. Select 10% of chromosomes from roulette wheel selection
# n_parents=[GA.rouletteWheelSelection() for _ in range(round(len(population)*0.1))]
# #Ensure the parents used to crossover is even number
# n_parents=n_parents if n_parents%2==0 else n_parents-1 
