from SupplyChain import SupplyChain
import random
import numpy as np

class Genetic_Algorithm():
    #random.seed(42)
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        self.sc=SupplyChain('5-10','TYPE_I')
        #TODO rmb to change back NO_OF_RETAILER & DC

    #=======================================================================================================
    def initialPopulation(self):
        '''Step 1: Initiating first population'''
        def generateX(chromosome):
            '''Matrix X is generated for each chromosome'''
            #=np.zeros((self.sc.NO_OF_RETAILER,self.sc.NO_OF_DC)).astype(int)
            X=np.zeros((5,4)).astype(int)
            for idx,dc in enumerate(chromosome):
                X[idx][dc-1]=1
            return X
        
        def generateY(X):
            '''Matrix Y is generated based on X'''
            #Y=np.zeros(self.sc.NO_OF_DC).astype(int).tolist()
            Y=np.zeros(4).astype(int).tolist()
            #for j in range(self.sc.NO_OF_DC):
            for j in range(4):
            #Loop each retailer whether it got assign to the DC 
                #for i in range(self.sc.NO_OF_RETAILER):
                for i in range(5):
                    if (X[i][j]==1):
                        Y[j]=1 
            return Y

        def generateChromosome():
            '''Generating chromosomes based on population size'''
            #chromosome=[random.randint(1,self.sc.NO_OF_DC) for i in range(self.sc.NO_OF_RETAILER)]
            chromosome=[random.randint(1,4) for i in range(5)]
            return chromosome
        #return [generateChromosome() for _ in range(self.POP_SIZE)]

        population=[generateChromosome() for _ in range(4)]
        X=[generateX(population[idx]) for idx in range(len(population))]
        Y=[generateY(X[idx]) for idx in range(len(population))]        
        print(population)
        print(X)
        print(Y)
    #=======================================================================================================
    def evaluateChromosome(self):
        '''Step 2: Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #self.sc.calcTotalCost(X,Y,s,Q)
        pass

    def elitism(self):
        '''Step 3: Retaining the best individuals in a gen unchanged in the next gen'''
        pass

    

    def crossOver(self):
        def rouletteWheelSelection(pop_parents):
            selection_chromosomes=[]
            #Iterate based on 80% chromosomes from population
            for _ in range(round(len(population)*0.8)):
                #From 80% chromosome
                elements=random.sample()


            pass
        
        population=[[2, 4, 3, 3, 2], [2, 3, 1, 1, 4], [1, 3, 3, 3, 1], [4, 1, 4, 1, 3]]
        '''Step 5: Crossover 2 parents to generate new offspring'''
        #Random selection of a pair of chromosome from population
        #80% of chromosome are selected using roulette wheel
        pop_parent1=random.randint(0,round(len(population)*0.8))
        pop_parent2==random.randint(0,round(len(population)*0.8))
        #Ensure that the parents are not duplicated
        pop_parent2=random.randint(0,round(len(population)*0.8)) if pop_parent2==pop_parent2 else pop_parent2
        n_parent1=rouletteWheelSelection(pop_parent1)
        n_parent2=rouletteWheelSelection(pop_parent2)
        #10% of genes from selected chromosomes are chosen

        pass

    def mutation(self):
        '''Step 6: Mutation used to maintain the genetic diversity of the chromosomes'''
        #Mutation operator in GA avoids convergence to local optimum and diverfies the population
        #Replacing a gene with a randomly selected number according to the parameter's boundaries

        pass

    def evaluateOffsprings(self):
        '''Step 7: Evaluate the performance of offsprings'''
        pass

    # population=self.generateChromosome()
    # print(population)

    
GA=Genetic_Algorithm(10000,50,100,0.8,0.2)
#GA.initialPopulation()
#GA.rouletteWheelSelection()
#GA.crossOver()

