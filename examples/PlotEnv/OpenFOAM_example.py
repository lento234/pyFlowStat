#! /usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
from pyFlowStat.PointProbe import PointProbe
#plt.ion()

path=r'Data/10/U'
pt = PointProbe()
pt.readFromOpenFoam([0.3,-0.3,0.05],path)

plt.figure('Standard plot')
plt.plot(pt.data['t'],pt.data['U'])
plt.grid(True)
plt.xlabel('Time $[s]$')
plt.ylabel('Velocity $[m/s]$')
plt.legend(('$U_x$','$U_y$','$U_z$'))
plt.savefig('figureStandard.pdf')
plt.show(block=False)

from pyFlowStat import plotEnv

# Custom plot environment
plotEnv.setupPlotEnv(numColors=3,style='ticks')

plt.figure('Customized plot')
plt.plot(pt.data['t'],pt.data['U'])
plt.xlabel('Time $[s]$')
plt.ylabel('Velocity $[m/s]$')
plotEnv.cleanupFigure(despine=True, tightenFigure=True, addMarkers=False, 
					  addLegend=True, labels=['$U_x$','$U_y$','$U_z$'], 
					  legendLoc=1)
plt.savefig('figureCustom.pdf')
