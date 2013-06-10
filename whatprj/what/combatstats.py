'''
Created on Feb 4, 2013

@author: khooks
'''
#import numpy as np
#from numpy import *
#from pylab import * 

#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#from collections import defaultdict
from damagetable import *



class hitstat(object):

    def __init__(self, DEF=1, attack=1):
         
        self.attack = attack
        self.DEF = DEF     
        
        
class attacksToKill(object):
    
    def __init__(self):
        pass
    

class hitsToKill(object):
    
    def __init__(self, ndice):
        self.ndice = ndice
        
        self.PMA = np.arange(1, 20, 1) #pow minus arm
        self.modelHealth = np.arange(1, 36, 1 )
        self.dt = damageTable(ndice)
          
    def avgHitsToKillPMA(self, powMinusARM, health):
        if self.dt.dmgFromPMA(powMinusARM) <= 0: return 36
              
        return health / self.dt.dmgFromPMA(powMinusARM) 
    
    def avgHitsToKill(self, armMinusPow, health):
        powMinusArm = -(armMinusPow)
        return self.avgHitsToKillPMA(powMinusArm, health)
        
    def __array__(self):
        
        N = len(self.powMinusARM) #rows
        M = len(self.modelHealth) #columns
        
        s = (N, M)
        
        z = np.zeros(s, dtype='float')
        
        #print z.shape
        
        for (x, y), value in np.ndenumerate(z):
            if( x < 0.001 ): z[x][y] = 1000
            else:
                z[x][y] = y / self.dt.dmgFromPMA( x )    
        return z
    
if __name__ == '__main__':
    #dmg is based on pow-arm but we want to plot w/ respect to increasing armor
    htk = hitsToKill(3)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.arange( -6, 10, 1)  #armminuspow
    print(x)
    y = np.arange( 1, 9, 1)    #health 
    print(y)
    
    X, Y = np.meshgrid(x, y)

    zs = np.array( [ htk.avgHitsToKill(x, y) for x, y in zip(np.ravel(X), np.ravel(Y)) ])
    
    Z = zs.reshape(X.shape)
    
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.Paired)
    
    
    ax.set_xlabel('ARM-POW')
    ax.set_ylabel('Health')
    ax.set_zlabel('Hits to Kill (average)')
    
    plt.show()   