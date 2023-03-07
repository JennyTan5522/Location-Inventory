from SupplyChain import SupplyChain
import random
from random import sample
import numpy as np

class Genetic_Algorithm():
    #random.seed(42)
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        #TODO rmb to change back NO_OF_RETAILER & DC

    #=======================================================================================================
    def initialPopulation(self,sc):
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

        self.population=[generateChromosome() for _ in range(self.POP_SIZE)]
        self.X=[generateX(self.population[idx]) for idx in range(len(self.population))]
        self.Y=[generateY(self.X[idx]) for idx in range(len(self.population))]    
        print(population)  
        print(X)
        print(Y)  
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
    def crossOver(self):
        '''Step 5: Crossover 2 parents to generate new offspring'''
        def rouletteWheelSelection(self):
            fitness=0 #TODO replace to fitness value
            #1. Random selection of 80% chromosomes from population
            chromosomesSample=sample(self.population,round(len(self.population)*0.8))
            #Calculate cumulative sum of fitness from 80% selected chromosomes
            cumulativeSum=np.cumsum(self.population) #TODO population change to 'fitness'
            #Generate a random number between 0 and cumulativeSum, choose the individual with cumulativeSum < fitness
            random=cumulativeSum*np.random.rand()
            index=np.argwhere(random<=cumulativeSum)
            return index[0][0]
        
        #2. Select 10% of chromosomes form roulette wheel selection
        n_parents=[rouletteWheelSelection() for _ in range(round(len(self.population)*0.1))]
        
        print(n_parents)

        #3. Ensure that the parents selected are not duplicated
        

    #=======================================================================================================
    def mutation(self,childs):#Take generated childs from the crossover step
        '''Step 6: Mutation used to maintain the genetic diversity of the chromosomes'''
        #Mutation operator in GA avoids convergence to local optimum and diverfies the population
        #Replacing a gene with a randomly selected number according to the parameter's boundaries
        for i in range(len(self.population)):
            chromosome=self.population[i]
            idx1=random.randint(0,len())

        pass

    def evaluateOffsprings(self):
        '''Step 7: Evaluate the performance of offsprings'''
        pass



    
GA=Genetic_Algorithm(10000,50,100,0.8,0.2)
# GA.initialPopulation()
#GA.rouletteWheelSelection()
# GA.crossOver()

sc=SupplyChain('5-10','TYPE_I')
    
population=GA.initialPopulation(sc)
print(population)      
# population=self.generateChromosome()
# print(population)