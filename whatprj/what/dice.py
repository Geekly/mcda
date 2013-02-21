'''
Created on Jan 30, 2013

@author: khooks
'''
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from numpy import *


class dice(object):
    '''
    classdocs
    '''
    @staticmethod
    def chancetorollXorhigher(ndice, x):
    
    @staticmethod
    def rolld6(ndice):
        result = 0.0
        nrolls = 10000
        np.dtype('int16')
        dice = np.zeros(shape=(nrolls, ndice + 1), dtype='int16')
        #print dice
        
        np.set_printoptions(threshold='nan')
        
        for x in range (0, nrolls):
            
            for n in range (0, ndice):
               
                dice[x, n] = random.randint(1,7)
                dice[x, ndice] = dice[x,n] + dice[x, ndice]  #last column becomes the sum of the rest of the dice
                
        #print dice  
        rawdata =  dice[:,ndice]    
        #hist, edges = np.histogram(rawdata, bins=17, range=(2.5, 18.5))  
        return rawdata

    def __init__(self):
        '''
        Constructor
    
        '''
        pass
    
    
    
if __name__ == '__main__':
    
    ndice = 3
    
    data = dice.rolld6(ndice)
    #print data
    
    minedge = ndice -.5
    maxedge = ndice*6 +.5
    numbins = ndice * 6 - (ndice - 1)
    print "minedge: " + str(minedge)
    print "maxedge: " + str(maxedge)
    print "numbins: " + str(numbins)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    n, bins, patches = ax.hist(data, numbins, normed=1, facecolor='green', alpha=0.75)
    print n
    print bins
    print patches
    #print n
    #print bins
    #print patches
    #bincenters = 0.5*(bins[1:]+bins[:-1])
    #y = mlab.normpdf(bincenters, 100, 15)
    
    plt.show()