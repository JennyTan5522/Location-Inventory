from SupplyChain import SupplyChain
import random
import numpy as np

class Genetic_Algorithm():
    random.seed(42)
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        self.sc=SupplyChain('5-10','TYPE_I')
        self.sc.NO_OF_DC

    def initialPopulation(self):
        def generateX(chromosome):
            '''Matrix X is generated for each chromosome'''
            X=np.zeros((self.sc.NO_OF_RETAILER,self.sc.NO_OF_DC)).astype(int)
            for idx,dc in enumerate(chromosome):
                X[idx][dc-1]=1
            return X
        
        def generateY(X):
            '''Matrix Y is generated based on X'''
            Y=np.zeros(self.sc.NO_OF_DC).astype(int).tolist()
            for j in range(self.sc.NO_OF_DC):
            #Loop each retailer whether it got assign to the DC 
                for i in range(self.sc.NO_OF_RETAILER):
                    if (X[i][j]==1):
                        Y[j]=1 
            return Y

        def generateChromosome():
            '''Step 1: Initiating first population'''
            chromosome=[random.randint(1,self.sc.NO_OF_DC) for i in range(self.sc.NO_OF_RETAILER)]
            X=generateX(chromosome)
            Y=generateY(X)
            return chromosome
        return [generateChromosome() for _ in range(self.POP_SIZE)]
    
    def evaluateChromosome(self):
        '''Step 2: Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #self.sc.calcTotalCost(X,Y,s,Q)
        pass

    def elitism(self):
        '''Step 3: Retaining the best individuals in a gen unchanged in the next gen'''
        pass

    def rouletteWheelSelection(self):
        '''Step 4: Select the parents using roulette wheel selection method'''
        pass

    def crossOver(self):
        '''Step 5: Crossover 2 parents to generate new offspring'''
        pass

    def mutation(self):
        '''Step 6: Mutation used to maintain the genetic diversity of the chromosomes'''
        pass

    def evaluateOffsprings(self):
        '''Step 7: Evaluate the performance of offsprings'''
        pass

    # population=self.generateChromosome()
    # print(population)

    
GA=Genetic_Algorithm(10000,50,100,0.8,0.2)
population=GA.initialPopulation()
print(len(population))