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
from plotter import Plotter


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
    



    
def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
    #~ dh = DataHolder('qt_mpl_data.csv')
    #~ print dh.data
    #~ print dh.get_series_data('1991 Sales')
    #~ print dh.series_names()
    #~ print dh.series_count()