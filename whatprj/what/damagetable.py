'''
Created on Jan 31, 2013

@author: khooks
'''
import numpy as np
from numpy import *
from pylab import * 

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


from collections import defaultdict

class dmgstat(object):
    '''
    classdocs
    Usage of this class eliminates errors related to swapping ARM and POW in the function calls
    '''
    def __init__(self, ARM=1, POW=1):
        '''
        Constructor
        '''
        self.POW = POW
        self.ARM = ARM

class damageTable(object):
    '''
    classdocs
    '''

    def __init__(self, numdice, armMin = 9, armMax = 22, powMin = 10, powMax = 19):
        '''
        Constructor
        X, N - POW
        Y, M - ARM
        
        '''        
        self.numdice = numdice
                
        self.armRange = range(armMin, armMax+1)
        self.powRange = range(powMin, powMax+1)
        
        self.diceavg = numdice*3.5
        
        #self.damageTable = defaultdict(defaultdict)
        
        #self.calcDamageTable()
        
    def calcDamageTable(self):        
        expectedDmg = 0.0      
        for ARM in self.armRange:
            for POW in self.powRange:
                expectedDmg = self.diceavg + POW - ARM 
                if expectedDmg < 0.0: expectedDmg = 0.0
                self.damageTable[ARM][POW] = expectedDmg
                
        #print self.damageTable
            
    def expectedDamage(self, dmgstat):
        expectedDmg = dmgstat.POW - dmgstat.ARM + self.diceavg
        if expectedDmg < 0.0: expectedDmg = 0.0
        return expectedDmg
    
    def dmg(self, ARM, POW):
        
        return self.expectedDamage( dmgstat(ARM, POW) )
    
    def dmgFromPMA(self, powMinusArm):
        
        return self.diceavg + powMinusArm

    
    def __array__(self):
        
        N = len(self.armRange) #rows
        M = len(self.powRange) #columns
        
        s = (N, M)
        
        z = np.zeros(s, dtype='float')
        #print z.shape
        
        for (x, y), value in np.ndenumerate(z):
            z[x][y] = self.expectedDamage ( dmgstat(x, y) )
            #z[x][y] = self.damageTable[x + self.armRange[0]][y + self.powRange[0]]
            #print (x, y)
            #print z[x][y]
        print z
        #need to map ranges starting at zero to use a typical array notation    
        #for key1, row in dt.damageTable.iteritems():
        #    for key2, value in row.iteritems():
        #        print  str(value), 
        #        z[key1-self.armRange[0]][key2-self.powRange[0]] = value
        #    print
        return z         
            
if __name__ == '__main__':

    dt = damageTable(3)
    
    print dt.__array__()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.arange( dt.armRange[0], dt.armRange[-1]+1, 1)
    y = np.arange( dt.powRange[0], dt.powRange[-1]+1, 1)
    
    X, Y = np.meshgrid(x, y)

    zs = np.array( [ dt.dmg(x, y) for x, y in zip(np.ravel(X), np.ravel(Y)) ])
    
    Z = zs.reshape(X.shape)
    
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.Paired)
    
    ax.set_xlabel('ARM')
    ax.set_ylabel('POW')
    ax.set_zlabel('Expected Dmg')
    
    plt.show()     
