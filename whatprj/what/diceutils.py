'''
Created on Jan 31, 2013

@author: khooks
'''
from collections import Counter

class diceset(object):
    '''
    classdocs
    '''  
    def __init__(self, ndice):
        '''
        Constructor
        '''
        self.ndice = ndice
        self.combos = []
        for d in self.dicecombos():
            self.combos.append(d)
        self.counter = Counter(self.combos)
      
        self.dicefreqs = dict()  #{ (freq, cumulativefreq),... }
          
        self.calcfreqs()  #dict
       

    def calcfreqs(self):
       
        ncombos =  sum(self.counter.values())
        
        keys = sorted(self.counter.iterkeys()) #get a sorted list, just in case 
        #print keys    
       
        for combo in keys:  #determine the frequency of occurrence for each combination
            
            count = float(self.counter[combo])
            #print key
            freq = count/ncombos
            
            self.dicefreqs[combo] = [freq, 0.0]
        
        self.dicefreqs[keys[0]][1] = self.dicefreqs[keys[0]][0]
        for combo in keys[1:]: #don't evaluate the last combo
            oldsum = self.dicefreqs[combo-1][1]
            #debugout("oldsum", oldsum)
            newsum = oldsum + self.dicefreqs[combo][0]
            self.dicefreqs[combo][1] = newsum

        
    def dicecombos(self):
        return self.permutate(self.ndice)
        
    def permutate(self, n):

        sides = [1,2,3,4,5,6]
        
        if n == 1:
            for i in sides:
                yield i
        else:
            for i in sides:
                for j in self.permutate(n - 1):
                    yield i + j
                    
    def equalorhigher(self, value):
        chance = 0.0
        
        if value in self.combos:
            chance = 1.0 - self.dicefreqs[value][1]
            return chance
            pass
        
        else: 
            raise IndexError("Index " + str(value) + " is not a valid location")
                    #

def debugout(name, value):
    print str(name) + ": " + str(value)
   

if __name__ == '__main__':
    
    #for i in combos(1): print i
    roll2d6 = diceset(2)

    
    roll3d6 = diceset(3)
    #print threeD6.dicefreqs
    #counter = Counter(results)
    print roll3d6.equalorhigher(7)
    
    for item in roll2d6.dicefreqs:
        print ( str(item) + ": " + str(roll2d6.dicefreqs[item][0]) + ", " + str(roll2d6.dicefreqs[item][1]) )
    
    