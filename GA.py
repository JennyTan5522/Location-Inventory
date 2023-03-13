from SupplyChain import SupplyChain 
import random
import numpy as np

class GA:
    
    def __init__(self,MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,CX_PERC,sc:SupplyChain,random_state=42):
        random.seed(random_state)
        self.MAX_GENERATION=MAX_GENERATION
        self.POP_SIZE=POP_SIZE
        self.MAX_SAME_ANSWER_PRODUCED=MAX_SAME_ANSWER_PRODUCED
        self.CROSS_RATE=CROSS_RATE
        self.GEN_MUT_RATE=GEN_MUT_RATE
        self.CX_PERC=CX_PERC
        self.sc=sc
        self.INDIVIDUAL_LENGTH=self.sc.NO_OF_RETAILER

    def generateChromosome(self):
        '''Generating chromosomes based on the size of DC and retailer'''
        #NO_OF_DC+1 cater for the dummy DC
        chromosome=[random.randint(1,self.sc.NO_OF_DC+1) for i in range(self.sc.NO_OF_RETAILER)]
        return chromosome
    
    def generateX(self,chromosome:list):
        '''Matrix X is generated for each chromosome'''
        X=np.zeros((self.sc.NO_OF_RETAILER,self.sc.NO_OF_DC)).astype(int)
        for idx,dc in enumerate(chromosome):
            if dc<=self.sc.NO_OF_DC:
                X[idx][dc-1]=1 #If not dc
                #NO_OF_DC=5 DUMMY_DC=6
        return X
      
    def generateY(self,X):
        '''Matrix Y is generated based on X'''
        return [1 if j>0 else 0 for j in np.sum(X,axis=0)]
        
    def evaluateChromosome(self,chromosome): 
        '''Evaluating chromosomes: Using fitness function (Min TC form SC)'''
        #Generate X and Y
        X=self.generateX(chromosome)
        Y=self.generateY(X)

        #Based on X then calc DC arrival rate
        self.sc.calcDcArrivalRate(X)

        #Compute optimum s and Q (a list with j elements) 
        optimalS,optimalQ=self.calcOptimumSQ(X,Y)
        #Check constraint, if not fulfill

        #Then pass to fitness: Check X or Y whether dummy DC is got open or not, if got add penalty cost
        fitness=self.sc.penaltyCost(chromosome)+self.sc.calcTotalCost(X,Y,optimalS,optimalQ)
        return fitness

    def rouletteWheelSelection(self,ranked_population):
        #Sum of population fitness
        sumPopulationFitness=np.sum([fitness[0] for fitness in ranked_population])
        #Compute each chromosome's probability 
        chromosome_prob=[fitness[0]/sumPopulationFitness for fitness in ranked_population]
        #Making the prob for minimization prob
        chromosome_prob=1-np.array(chromosome_prob)
        chromosome_prob=chromosome_prob.tolist()
        #Generate random r, if a current sum>r, then select that chromosome
        return ranked_population[chromosome_prob.index(np.random.choice(chromosome_prob))][1]

    def cross_over(self,child1,child2):
        #Based on 10% then select k sample from parent1
        cxPos=random.sample(range(len(child1)),int(len(child1)*self.CX_PERC))
        for idx in cxPos:
            temp=child1[idx]
            child1[idx]=child2[idx]
            child2[idx]=temp
        return child1,child2

    def mutation(self,child):
        #Position to mutate
        r=random.randint(0,len(child)-1)
        #If current parent value same as the replace DC, a new random DC will be generated;else break the loop and mutate the gene 
        choiceRange=[j for j in range(1,self.sc.NO_OF_DC+1) if j!=child[r]]
        child[r]=random.choice(choiceRange)
        return child
    
    def newGeneration(self):
        history={} #Save 'average' and 'best fitness' as a key
        best_individual=(float('inf'),None) #Fitness
        
        #Step 1: Initiating first population
        self.population=[self.generateChromosome() for _ in range(self.POP_SIZE)]

        for iter in range(self.MAX_GENERATION):
            ranked_population=[]
            
            #Step 2: Evaluating chromosome
            for chromosome in self.population:
                ranked_population.append((self.evaluateChromosome(chromosome),chromosome)) #(fitness,chromosome)

            #Rank from low to high -> The lowest the better
            ranked_population.sort()

            #Compare the current population's best individual with the current best individual
            if(ranked_population[0][0]<best_individual[0]):
                best_individual=ranked_population[0]
                
            #Update history
            history[iter]={'Avg':np.mean([ind[0] for ind in ranked_population]),'Best':ranked_population[0][0]}

            n_parents=self.POP_SIZE-int(self.POP_SIZE*0.2) #80% for parent selection
            #Make sure n_parents is even number
            if n_parents%2!=0:
                n_parents+=1
                #Step 3: Elitism - Select the top 20% from ranked_pop which use to remain for next generation
                elitism_population=[ind[1] for ind in ranked_population[:int(self.POP_SIZE*0.2)-1]]  #TODO Next round no need re-evaluate
            else:
                elitism_population=[ind[1] for ind in ranked_population[:int(self.POP_SIZE*0.2)]]  #TODO Next round no need re-evaluate
            '''
            X - reserved
            X - reserved
            X - selection, crossover, mutation
            X - selection, crossover, mutation 
            X - selection, crossover, mutation
            Select -> CX? Yes -> Partner for crossover
                           No -> Skip
            '''
            new_population=[]
            for i in range(0,n_parents):
                #Select parent first then only perform cross over
                #Step 4: Parent selection - Select 80% from ranked_pop for parent selection
                while(True):
                    parent1=self.rouletteWheelSelection(self.population,ranked_population)
                    parent2=self.rouletteWheelSelection(self.population,ranked_population)
                    if parent1!=parent2:
                        break
                
                #Step 5: Crossover - Undergo crossover if less or equal to 0.8
                if random.uniform(0,1)<=self.CROSS_RATE:
                    child1,child2=self.cross_over(parent1,parent2)
                else:
                    child1=parent1
                    child2=parent2

                #Step 6: Mutation - Undergo mutation if less or equal to 0.2
                if random.uniform(0,1) <= self.GEN_MUT_RATE:
                    child1=self.mutation(child1)
                if random.uniform(0,1) <= self.GEN_MUT_RATE:
                    child2=self.mutation(child2)    
                
                #Append child into new population
                new_population.append(child1) 
                new_population.append(child2)

            #New population generated
            self.population=elitism_population+new_population
        return best_individual,history

    def calcOptimumSQ(self,X,Y):
        '''Find optimal S0j, Q0j and costs'''
        #-- Step1: Find Qmin for each DC --
        Qmin=list(self.sc.calcQmin()[0])
        #-- Step 2:Calculate Q0 and s0 to find optimal Q0 and s0 --
        #Loop for every DC's s0 and q0
        s0List=[] 
        q0List=[]
        for j in range(self.sc.NO_OF_DC):#Loop every DC to calculate
            breakQFlag=False #If found correct then break
            minValue=9999 #In case cannot found=0, then found the nearest min value
            targetS0=None 
            targetQ0=None
            for q0 in reversed(range(2,int(Qmin[j]))): #Loop q0, starting from q1-1 reversed=1259
                #For every q0 test for every s0
                for s0 in range(1,q0):#X only take one column try 1-1258
                    diff=self.sc.calcTotalCost(X,Y,s0+1,q0,j+1)-self.sc.calcTotalCost(X,Y,s0,q0,j+1)
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
                diff=self.sc.calcTotalCost(X,Y,0,q1+1,j+1)-self.sc.calcTotalCost(X,Y,0,q1,j+1)
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
            tcCost1=self.sc.calcTotalCost(X,Y,s0List,q0List,j+1)
            tcCost2=self.sc.calcTotalCost(X,Y,0,q1List,j+1)
            if(tcCost1<tcCost2):
                #Save as tuple
                optimalS.append(s0List[j])
                optimalQ.append(q0List[j])
            else:#tcCost1>tcCost2
                optimalS.append(s0List[j])
                optimalQ.append(q0List[j])
        return optimalS,optimalQ

if __name__ == "__main__":        
    sc=SupplyChain('5-10','TYPE_I')
    MAX_GENERATION=2
    POP_SIZE=20
    MAX_SAME_ANSWER_PRODUCED=100
    CROSS_RATE=0.8
    GEN_MUT_RATE=0.2
    CX_PERC=0.1
    GA=GA(MAX_GENERATION,POP_SIZE,MAX_SAME_ANSWER_PRODUCED,CROSS_RATE,GEN_MUT_RATE,CX_PERC,sc)
    GA.newGeneration()


