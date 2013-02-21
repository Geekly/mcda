'''
Created on Feb 1, 2013

@author: khooks
'''
import diceutils

class hitTable(object):
    '''
    classdocs
    '''

    def __init__(self, ndice, defMin=5, defMax=20, atkMin=1, atkMax=12):
        '''
        Constructor
        '''
        self.ndice = ndice
        
        self.defRange = range(defMin, defMax+1)
        self.atkRange = range(atkMin, atkMax+1)
        
        self.hitTable = dict()
                        
        self.dice = diceutils.diceset(ndice)
        self.calcHitTable()
        
    def calcHitTable(self):
        for d in self.defRange:
            for a in self.atkRange:
                self.hitTable[d,a] = self.chanceToHit(d, a)
    
    
    def chanceToHit(self, defense, atk):
        successRoll = defense - atk
        if ( successRoll < self.ndice): successRoll = self.ndice
        if ( successRoll > (self.ndice * 3)): successRoll = self.ndice * 3
        chanceToHit = self.dice.equalorhigher(successRoll)    
        return chanceToHit
    
    def __array__(self):
        
        N = len(self.defRange) #rows
        M = len(self.atkRange) #columns
        
        s = (N, M)
        
        z = np.zeros(s, dtype='float')
        
        print z.shape
        
        for (x, y), value in np.ndenumerate(z):
            z[x][y] = self.hitTable[x + self.defRange[0]][y + self.atkRange[0]]
            
    def __str__(self):
        
        row_format = "{:>15" * (len(self.defRange))
        for d in self.defRange:
            
            for a in self.atkRange:
                print ("DEF: " + str( d ) + ", ATK: " + str(a) + ", CTH:" + str(self.hitTable[d,a]) )   
        
if __name__ == '__main__':
    
    ht = hitTable(2)
    
    for entry in ht.hitTable.items():
        print entry
    print ht