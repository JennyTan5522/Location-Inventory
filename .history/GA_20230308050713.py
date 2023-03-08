import SupplyChain
import random
import numpy as np

class Genetic_Algorithm:
    random.seed(42)
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        self.sc=sc
        self.INDIVIDUAL_LENGTH=self.sc.INDIVIDUAL_LENGTH
        #TODO rmb to change back NO_OF_RETAILER & DC

    #=======================================================================================================
    def initialPopulation(self):
        '''Step 1: Initiating first population'''
        def generateChromosome(self):
            '''Generating chromosomes based on population size'''
            #NO_OF_DC+1 cater for the dummy DC
            chromosome=[random.randint(1,sc.NO_OF_DC+1) for i in range(sc.NO_OF_RETAILER)]
            return chromosome
        return [generateChromosome() for _ in range(self.POP_SIZE)]
        
    #=======================================================================================================
    def evaluateChromosome(self):
        '''Step 2: Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #self.sc.calcTotalCost(X,Y,s,Q)
        #In population then loop for each chromosome, then find the fitness
        pass

    #=======================================================================================================
    def elitism(self):
        '''Step 3: Retaining the best individuals in a gen unchanged in the next gen'''
        pass

    #=======================================================================================================
    '''Step 4: Parents selection based on roulette wheel selection'''
    def rouletteWheelSelection(self):
        pass

    #=======================================================================================================
    def crossOver(self,n_parents):
        '''Step 5: Crossover 2 parents to generate new offspring'''
        pass
    #=======================================================================================================
    def inversion_mutation(population,chromosome):
        '''Step 6: Mutation used to maintain the genetic diversity of the chromosomes'''
        #     #Mutation operator in GA avoids convergence to local optimum and diverfies the population
        #     #Replacing a gene with a randomly selected number according to the parameter's boundaries
        pass

    #=======================================================================================================
    def evaluateOffsprings(self):
        '''Step 7: Evaluate the performance of offsprings'''
        #Best chromosome, everytime will check whether it will better than best chromosome
        pass

    #=======================================================================================================
    def run(self):
        #Start initialization
        self.population=self.initialPopulation()
        print(self.population)
        pass

sc=SupplyChain('5-10','TYPE_I')
MAX_GENERATION=10000
POP_SIZE=20
MAX_SAME_ANSWER_PRODUCED=100
CROSS_RATE=0.8
GEN_MUT_RATE=0.2
GA=Genetic_Algorithm(MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,sc)
GA.run()


# X=[GA.generateX(population[idx]) for idx in range(len(population))]
# Y=[GA.generateY(X[idx]) for idx in range(len(population))]    
# print(population)  
# print(X)
# print(Y)  
# #2. Select 10% of chromosomes from roulette wheel selection
# n_parents=[GA.rouletteWheelSelection() for _ in range(round(len(population)*0.1))]
# #Ensure the parents used to crossover is even number
# n_parents=n_parents if n_parents%2==0 else n_parents-1 
