import sys
import math
import random as r

class ClickBaitIdentifier:
    
    def __init__(self):
        self.input_vector = []
        self.weight_vector = []
        self.word_weight = {}
        

    def setInput(self,title):
        self.input_vector = title.split()

    def setWeight(self):
        for i in range(len(self.input_vector)):
            self.weight_vector.append(self.word_weight[self.input_vector[i]])
    
    def calcWeights(self):
        total = 0
        for i in range(len(self.input_vector)):
            total += self.input_vector[i] * self.weight_vector[i]
        return

    #Functions to be used
    def xSquared(self,x = 0):
        return x**2

    def normalDist(self,u_mean,stddev,x):
        return (1/(stddev*math.sqrt(2*math.pi)))*math.exp(-(x-u_mean)**2/(2*stddev**2))

    def cdfNormal(self,mean,stddev,x):
        return (1.0 + math.erf((x-mean)/(stddev*math.sqrt(2))))/2
    
    def sigmoid(self,z):
        return math.tanh(z)
        #return 1/(1+math.exp(-z))
    
    #End Functions
    
    def firstDerivative(self,x,*func):
        #f(x+h) - f(x-h)/2h
        #For testing purposes I am only passing a value and hard coding the formula
        h = math.sqrt(sys.float_info.epsilon)
        return (func(x+h) - func(x-h))/(2*h)

    def isSeen(self):
        """
        Tests to see if the word in the title has bee seen before
        If it has not then it will be added to the dictionary with a random weight based off of the CDF of the Normal distribution
        """
        for i in range(len(self.input_vector)):
            
            print("Enter loop -- word : {}".format(self.input_vector[i]))
                  
            if not(self.input_vector[i] in self.word_weight):
                print("Is not in dictionary")
                self.addToDict(self.input_vector[i],self.cdfNormal(.5,1,r.random()))
                
    
    
    def addToDict(self,word,weight):
        self.word_weight[word] = weight
       
    #Methods to write

    def testTitle(self):
        """
        This is just the base testing method to see if an article is clickbait
        """
        pass

    def adjustWeight(self):
        pass
    
    def train(self):
        """
        Training will read from a file (train.txt) that will contain a list of titles with an accompanied boolean, true or false
        
        """
        pass

    def isClickbait(self):
        """
        Will sum up the three hidden layer neurons buzzword, number, and punctuation
        If it is above a certain level it will output true, it is clickbait, and 

        """
        pass

    def buzzwordNeuron(self):
        """
        If a word in the input_vector has a very high weight, then it will be considered a buzzword
        The presence of a buzzword will increase the likelyhood of the Neuron outputting a trigger value.
        Will also make a list of words that passed the buzzword threshold so their weights can be changed more
        """
        total = 0.0
        for i in range(len(self.input_vector)):
            total += self.weight_vector[i]
            
        return total/len(self.input_vector)

    def numberNeuron(self):
        """
        Clickbait titles tend to have a number in their title indicating the article is a list
        Having numbers will not be a major trigger since many real news stories have numbers, but clickbait seem to have numbers more frequently
        """
        pass

    def punctuationNeuron(self):
        """
        Question marks and hash tags will set this neuron off
        """
        pass

    """Both write and import dictionary will be used for persistant storage so that the program can be closed and reopened without loss of progress"""
    def writeToDict(self):
        f.open('dictionary.txt','w')
        f.close('dictionary.txt')
        pass
    
    def importDict(self):
        pass

    
    def __main__(self):
        a = [5,3,9]
        b = [1,4,7]
        setInput(a)
        setWeight(b)
        print(calcWeights())


    
