'''
Created on Mar 15, 2013

@author: khooks
'''

import numpy as np
from numpy import *
from pylab import *

from damagetable import *
from combatstats import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("WHAT - Warmahordes Attack Template")
        
        self.create_main_frame()
        self.update_ui()
        self.on_show()
        
    def update_ui(self):
        return
    
    def create_main_frame(self):
        self.main_frame = QWidget()
        
        plot_frame = QWidget()
        
        self.dpi = 100
        self.fig = Figure((6.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        self.axes = self.fig.add_subplot(111)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        log_label = QLabel("Data series:")
        self.series_list_view = QListView()
        #self.series_list_view.setModel(self.series_list_model)
        
        spin_label1 = QLabel('X from')
        self.from_spin = QSpinBox()
        spin_label2 = QLabel('to')
        self.to_spin = QSpinBox()
        
        spins_hbox = QHBoxLayout()
        spins_hbox.addWidget(spin_label1)
        spins_hbox.addWidget(self.from_spin)
        spins_hbox.addWidget(spin_label2)
        spins_hbox.addWidget(self.to_spin)
        spins_hbox.addStretch(1)
        
        self.legend_cb = QCheckBox("Show L&egend")
        self.legend_cb.setChecked(False)
        
        self.show_button = QPushButton("&Show")
        #self.connect(self.show_button, SIGNAL('clicked()'), self.on_show)

        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.canvas)
        left_vbox.addWidget(self.mpl_toolbar)

        right_vbox = QVBoxLayout()
        right_vbox.addWidget(log_label)
        right_vbox.addWidget(self.series_list_view)
        right_vbox.addLayout(spins_hbox)
        right_vbox.addWidget(self.legend_cb)
        right_vbox.addWidget(self.show_button)
        right_vbox.addStretch(1)
        
        hbox = QHBoxLayout()
        hbox.addLayout(left_vbox)
        hbox.addLayout(right_vbox)
        self.main_frame.setLayout(hbox)

        self.setCentralWidget(self.main_frame)
        
    def on_show(self):
        self.axes.clear()        
        self.axes.grid(True)
        
        has_series = False
        
        '''for row in range(self.series_list_model.rowCount()):
            model_index = self.series_list_model.index(row, 0)
            checked = self.series_list_model.data(model_index,
                Qt.CheckStateRole) == QVariant(Qt.Checked)
            name = str(self.series_list_model.data(model_index).toString())
            
            if checked:
                has_series = True
                
                x_from = self.from_spin.value()
                x_to = self.to_spin.value()
                series = self.data.get_series_data(name)[x_from:x_to + 1]
                self.axes.plot(range(len(series)), series, 'o-', label=name)
        
        if has_series and self.legend_cb.isChecked():
            self.axes.legend()
        '''
        self.canvas.draw()
        
class Plotter():
    
    @staticmethod
    def plotExpectedDamage(ndice):
        #plot ARM, POW, Expected Damage
        
        #htk = hitsToKill(2)
        dt = damageTable(ndice)
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
    
    @staticmethod    
    def plotHitsToKill(title):
        htk = hitsToKill(3)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d', title=title)
    
        x = np.arange( -6, 11, 1)  #armminuspow
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
        
    @staticmethod    
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
        print(X2)
        print(Y1)
        print(Y2)
        
        ax.scatter( 19, boostedhtk.avgHitsToKill(19 - POW, health), c='red', marker='o')
        ax.scatter( 22, boostedhtk.avgHitsToKill(22 - POW, health), c='red', marker='o')
        
        
        ax.plot (X2, Y1, label="Expected Damage", linewidth=2.5, c='blue')
        ax.plot (X2, Y2, label="Hits to Kill", linewidth=2.5, c='red')
        ax.plot ( [19, 19],[-1, boostedhtk.avgHitsToKill(19 - POW, health)], c='red' )
        ax.plot ( [22, 22],[-1, boostedhtk.avgHitsToKill(22 - POW, health)], c='red' )
            
            
        ax.legend(loc='upper left')
        plt.show()
        
    @staticmethod    
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
        print( X)
        print( Y1)
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
        
def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
            
