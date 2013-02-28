'''
Created on Jan 30, 2013

@author: khooks
'''

from diceutils import diceset
import numpy as np


from pylab import *    
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from combatstats import hitsToKill


from damagetable import *

def plot2():
    htk = hitsToKill(2)
    #dt = damageTable(2)
    dt = damageTable(2, 0, 30, 0, 30)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

     
    x = htk.PMA
    y = htk.modelHealth
       
    X, Y = np.meshgrid(x, y)

    zs = np.array( [ dt.dmg(x, y) for x, y in zip(np.ravel(X), np.ravel(Y)) ])
    
    Z = zs.reshape(X.shape)
    
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.Paired)
    
    ax.set_xlabel('ARM')
    ax.set_ylabel('POW')
    ax.set_zlabel('Expected Dmg')
    plt.show()

def plot1():
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111, title="Boosted POW 15's vs 32 Health", xlabel="ARM")
    
    boostedhtk = hitsToKill(3)
    dt = damageTable(3, 0, 30, 0, 30)

    dt.expectedDamage( dmgstat(19, 16) )
    
    
    POW = 15
    health = 32
    X2 = np.arange(15, 26, 1)
    Y1 = np.array( [ dt.expectedDamage( dmgstat(x, POW) ) for x in X2] )
    Y2 = np.array( [ boostedhtk.avgHitsToKill(x - POW, health)  for x in X2 ] )
    print X2
    print Y1
    print Y2
    
    ax.scatter( 19, boostedhtk.avgHitsToKill(19 - POW, health), c='red', marker='o')
    ax.scatter( 22, boostedhtk.avgHitsToKill(22 - POW, health), c='red', marker='o')
    
    
    ax.plot (X2, Y1, label="Expected Damage", linewidth=2.5, c='blue')
    ax.plot (X2, Y2, label="Hits to Kill", linewidth=2.5, c='red')
    ax.plot ( [19, 19],[-1, boostedhtk.avgHitsToKill(19 - POW, health)] )
        
        
    ax.legend(loc='upper left')
    plt.show()
    
def plotExpectedDamage():
    #plot ARM, POW, Expected Damage
    
    #htk = hitsToKill(2)
    dt = damageTable(2)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

     
    x = range(7, 23)
    y = range(10, 20)
       
    X, Y = np.meshgrid(x, y)

    zs = np.array( [ dt.dmg(x, y) for x, y in zip(np.ravel(X), np.ravel(Y)) ])
    
    Z = zs.reshape(X.shape)
    
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.Paired)
    
    ax.set_xlabel('ARM')
    ax.set_ylabel('POW')
    ax.set_zlabel('Expected Dmg, 2D6')
    plt.show()    
    
def plotHitsToKill(title):
    htk = hitsToKill(3)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', title=title)

    x = np.arange( -6, 11, 1)  #armminuspow
    print x
    y = np.arange( 1, 9, 1)    #health 
    print y
    
    X, Y = np.meshgrid(x, y)

    zs = np.array( [ htk.avgHitsToKill(x, y) for x, y in zip(np.ravel(X), np.ravel(Y)) ])
    
    Z = zs.reshape(X.shape)
    
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.Paired)
    
    
    ax.set_xlabel('ARM-POW')
    ax.set_ylabel('Health')
    ax.set_zlabel('Hits to Kill (average)')
    
    plt.show()     
    
def plot2DHTKfixedPOW(ndice, POW, health):
    
    
    fig = plt.figure()
    
    strtitle = "Boosted POW " + str(POW) + " vs " + str(health) + " Health"
    ax = fig.add_subplot(111, title=strtitle, xlabel="ARM")
    
    boostedhtk = hitsToKill(ndice)
    dt = damageTable(3, 0, 30, 0, 30)

    #dt.expectedDamage( dmgstat(19, 15) )
    
    
    #POW = 15
    #health = 56
    X2 = np.arange(16, 24, 1)
    Y1 = np.array( [ dt.expectedDamage( dmgstat(x, POW) ) for x in X2] )
    Y2 = np.array( [ boostedhtk.avgHitsToKill(x - POW, health)  for x in X2 ] )
    print X2
    print Y1
    print Y2
    
    ax.scatter( 19, boostedhtk.avgHitsToKill(19 - POW, health), c='red', marker='o')
    ax.scatter( 22, boostedhtk.avgHitsToKill(22 - POW, health), c='red', marker='o')
    
    
    ax.plot (X2, Y1, label="Expected Damage", linewidth=2.5, c='blue')
    ax.plot (X2, Y2, label="Hits to Kill", linewidth=2.5, c='red')
    ax.plot ( [19, 19],[-1, boostedhtk.avgHitsToKill(19 - POW, health)], c='red' )
    ax.plot ( [22, 22],[-1, boostedhtk.avgHitsToKill(22 - POW, health)], c='red' )
        
        
    ax.legend(loc='upper left')
    plt.show()
    
def plotPartialHTKwrtARM(ndice, POW, health):
    fig = plt.figure()
    
    strtitle = "Value of ARM, POW vs " + str(health) + " Health"
    ax = fig.add_subplot(111, title=strtitle, xlabel="ARM")
    
    boostedhtk = hitsToKill(ndice)
    dt = damageTable(3, 0, 30, 0, 30)

    #dt.expectedDamage( dmgstat(19, 15) )
    
    
    #POW = 15
    #health = 56
    X = np.arange(9, 18, 1)
    Y1 = np.array( [ health/((POW - x + 3.5*ndice)**2) for x in X] )
    Y2 = np.array( [ -health/((POW - x + 3.5*ndice)**2) for x in X] )
    Y3 = np.array( [ -1/(POW - x + 3.5*ndice) for x in X] )
    #Y2 = np.array( [ boostedhtk.avgHitsToKill(x - POW, health)  for x in X2 ] )
    print X
    print Y1
    #print Y2
    
    #ax.scatter( 19, boostedhtk.avgHitsToKill(19 - POW, health), c='red', marker='o')
    #ax.scatter( 22, boostedhtk.avgHitsToKill(22 - POW, health), c='red', marker='o')
    
    
    ax.plot (X, Y1, label="HTK/ARM", linewidth=2.5, c='blue')
    ax.plot (X, Y2, label="HTK/POW", linewidth=2.5, c='red')
    ax.plot (X, Y3, label="HTK/Health", linewidth=2.5, c='green')
    #ax.plot ( [19, 19],[-1, boostedhtk.avgHitsToKill(19 - POW, health)], c='red' )
    #ax.plot ( [22, 22],[-1, boostedhtk.avgHitsToKill(22 - POW, health)], c='red' )
        
        
    ax.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
 
    #plotHitsToKill("Boosted Hits To Kill, Infantry")
    plotPartialHTKwrtARM(2, 12, 1)