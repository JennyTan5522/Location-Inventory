import random
class Genetic_Algorithm:
    random.seed(42)
   
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE):
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE

    def initialPopulation():
        '''Step 1: Initiating first populaiton'''
        pass

    def evaluateChromosome():
        '''Step 2: Evaluating chromosomes'''
        pass

    def elitism():
        '''Step 3: Retaining the best individuals in a gen unchanged in the next gen'''
        pass

    def rouletteWheelSelection():
        '''Step 4: Select the parents using roulette wheel selection method'''
        pass

    def crossOver():
        '''Step 5: Crossover 2 parents to generate new offspring'''
        pass

    def mutation():
        '''Step 6: '''

        
GA=Genetic_Algorithm(10000,50,100,0.8,0.2)