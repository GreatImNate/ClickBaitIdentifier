import sys
import math
import re
import random as r

class ClickBaitIdentifier:
    
    def __init__(self):
        self.input_vector = []
        self.weight_vector = []
        self.word_weight = {}
        self.numeric_weight = 0.0
        self.punc_weight = 0.0
        self.learning_rate = 0.1

    #Used to re initialize the dictionary, and all the numeric weights to what they where previously
    def reInit(self):
        pass

    def clean(self):
        del self.weight_vector[:]
        del self.input_vector[:]
        pass
        
    def setNumericWeight(self):
        self.numeric_weight = self.cdfNormal(r.random())
        
    def setPuncWeight(self):
        self.punc_weight = self.cdfNormal(r.random())
        
    def setInput(self,title):
        temp = title.lower()
        self.input_vector = temp.split()

    def setWeight(self):
        for i in range(len(self.input_vector)):
            self.weight_vector.append(self.word_weight[self.input_vector[i]])
            if(self.input_vector[i].lower() == 'this'):
                print("weight of this being set with weight {}".format(self.word_weight['this']))
                
    
    def calcWeights(self):
        total = 0
        for i in range(len(self.input_vector)):
            total += self.input_vector[i] * self.weight_vector[i]
        return

    #Functions to be used

    def normalDist(self,u_mean,stddev,x):
        return (1/(stddev*math.sqrt(2*math.pi)))*math.exp(-(x-u_mean)**2/(2*stddev**2))

    def cdfNormal(self,x,mean = .5,stddev = 5):
        return (1.0 + math.erf((x-mean)/(stddev*math.sqrt(2))))/2
    
    def sigmoid(self,z):
        return math.tanh(z)
        #return 1/(1+math.exp(-z))
    
    #End Functions
    
    def firstDerivative(self,x,func):
        #f(x+h) - f(x-h)/2h
        #For testing purposes I am only passing a value and hard coding the formula
        h = math.sqrt(sys.float_info.epsilon)
        return (func(x+h) - func(x-h))/(2*h)

    def isSeen(self):
        """
        Tests to see if the word in the title has bee seen before
        If it has not then it will be added to the dictionary with a random weight based off of the CDF of the Normal distribution
        """
        pattern = re.compile('[\W_]+') #This will be incorporated possibly to cut out repeats in the dictionary just because a word had some character attached
        for i in range(len(self.input_vector)):
            
            #print("Enter loop -- word : {}".format(self.input_vector[i]))
                  
            if not(self.input_vector[i].lower() in self.word_weight):
                #print("Is not in dictionary")
                self.addToDict(self.input_vector[i],self.cdfNormal(r.random()))
                
    
    
    def addToDict(self,word,weight):
        self.word_weight[word] = weight
       
    #Methods to write

    def testTitle(self):
        """
        This is just the base testing method to see if an article is clickbait
        """
        
        self.isSeen()
        self.setWeight()
        self.setNumericWeight()
        self.setPuncWeight()
        weighted_sum = self.isClickbait()
        if (weighted_sum > 1.0):
            return True
        else:
            return False
        

    def adjustWeight(self,shift):
        for i in range(len(self.weight_vector)):
            self.weight_vector[i] = (self.weight_vector[i] + (shift))
    
    def train(self):
        """
        Training will read from a file (train.txt) that will contain a list of titles with an accompanied boolean, true or false
        """
        self.setPuncWeight()
        self.setNumericWeight()
        print("Opening File")
        with open('train.txt') as f:
            print("Beginning File")
            triggered = False
            for line in f:
                print("Reading line")
                if(line == "True\n") or (line == 'True'):
                    #print("the line readas true!")
                    shift = self.firstDerivative(self.isClickbait(),self.sigmoid) * self.learning_rate
                    
                    if(triggered == True):
                        #print("Correctly Identified - adjusting values")
                        #self.adjustWeight(shift)
                        for i in range(len(self.input_vector)):
                            if(self.input_vector[i] == 'this'):
                                print("found this - weight {}".format(self.word_weight['this']))
                                print(shift)
                            #print("adjusting weight value for key {} - previous value was {}".format(self.input_vector[i],self.weight_vector[i]))
                            self.weight_vector[i] = self.weight_vector[i] + shift
                            if(self.input_vector[i] == 'this'):
                                print("Weight stored in vector for this position {} :: {}".format(i,self.weight_vector[i]))
                            self.word_weight[self.input_vector[i].lower()] = self.weight_vector[i]
                            if(self.input_vector[i] == 'this'):
                                print("adjusted value now stored in dict {}".format(self.word_weight[self.input_vector[i].lower()]))                                
                            #print("adjusted weight value for key {} - is now {}".format(self.input_vector[i],self.weight_vector[i]))
                        triggered = False
                        self.clean()
                        
                    else:
                        for i in range(len(self.input_vector)):
                            if(self.input_vector[i].lower() == 'this'):
                                print("found this - weight {}".format(self.word_weight['this']))
                                print(shift)
                            #print("adjusting weight value for key {} - previous value was {}".format(self.input_vector[i],self.weight_vector[i]))
                            self.weight_vector[i] = self.weight_vector[i] + shift
                            if(self.input_vector[i] == 'this'):
                                print("Weight stored in vector for this position {} :: {}".format(i,self.weight_vector[i]))
                            self.word_weight[self.input_vector[i].lower()] = self.weight_vector[i]
                            if(self.input_vector[i] == 'this'):
                                print("adjusted value now stored in dict {}".format(self.word_weight[self.input_vector[i]]))                                
                            #print("adjusted weight value for key {} - is now {}".format(self.input_vector[i],self.weight_vector[i]))
                        triggered = False
                        self.clean()
                        
                else:
                    print(line)
                    self.setInput(str(line))
                    #print("Determining if clickbait ... " )
                    truth = self.isClickbait()
                    #print("summed total of all neurons is {}".format(truth))
                    if(truth > .50):
                        print("Title is clickbait!")
                        triggered = True
                    
                    
        

    def isClickbait(self):
        """
        Will sum up the three hidden layer neurons buzzword, number, and punctuation
        If it is above a certain level it will output true, it is clickbait, and 

        """
        self.isSeen()
        self.setWeight()
        total = self.buzzwordNeuron() + self.numberNeuron() + self.punctuationNeuron()
        return total

    def buzzwordNeuron(self):
        """
        If a word in the input_vector has a very high weight, then it will be considered a buzzword
        The presence of a buzzword will increase the likelyhood of the Neuron outputting a trigger value.
        Will also make a list of words that passed the buzzword threshold so their weights can be changed more
        """
        total = 0.0
        """
        Count the number of words that are above a certain threshold and keep a list of these words
        The count will be used as a modifier when being considered for how high of a value a is passed from neuron
        The list of repeated words will be stored, and when it comes time to modify the weights of these words they will recieve a higher weight change
        The idea behind this is that the more a word appears, the more and more likely it is a buzzword
        """
        for i in range(len(self.input_vector)):
            total += self.weight_vector[i]
            
        return total /len(self.input_vector)

    def numberNeuron(self):
        """
        Clickbait titles tend to have a number in their title indicating the article is a list
        Having numbers will not be a major trigger since many real news stories have numbers, but clickbait seem to have numbers more frequently
        Have a dynamic range for the values that are more likely to come up in a clickbait article
        by default will be from 10 to 30, if there are any values outside of this range it will expand the range slightly
        If a number in the title lies in the range, then a modifier will be passed to indicate higher probability that it is clickbait
        """
        count = 0
        for i in range(len(self.input_vector)):
            if self.input_vector[i].isnumeric():
                #print("Exists number in title")
                count += 1
        if (count >= 1):
            return self.numeric_weight/len(self.input_vector)
        else:
            return 0
                
            


    def punctuationNeuron(self):
        """
        Question marks and hash tags will set this neuron off
        """
        total = 0.0
        for i in range(len(self.input_vector)):
            if('#' in self.input_vector[i]) or ('?' in self.input_vector[i]):
                #print("punctuation found")
                total = self.punc_weight/len(self.input_vector)
        return total

        
    """Both write and import dictionary will be used for persistant storage so that the program can be closed and reopened without loss of progress
        The first line will be the numeric constants numeric weight, and the learning rate
    """
    def writeToDict(self):
        f.open('dictionary.txt','w')
        f.close('dictionary.txt')
        pass
    
    def importDict(self):
        f.open('dictionary.txt','r')
        f.close('dictionary.txt')
        
        pass

    
    def __main__(self):
        pass

    
