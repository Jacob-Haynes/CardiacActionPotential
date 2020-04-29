from solvePlot import DE
from gridCalc import Grid
from param import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as mpl
import matplotlib.animation
from tqdm import *
from scipy.integrate import odeint

'define heart array'
heart = np.zeros((pointTotal,gridSize,gridSize))
heart[:] = -0.07
active = np.zeros((pointTotal,gridSize,gridSize))
'define SA differential equation, and solve'
AP = DE(0.15, 2.5, 0.01, 0.06, 0 , 0, t,0)
AP.Solve()
sinoAtrial = AP.u

'Generate 3D arrays for heart and active'
for time2 in range(pointTotal):
    'set where SA is'
    for SAset in range(gridSize-1):
        heart[time2][SAset][0] = round(sinoAtrial[time2],3)
        active[time2][SAset][0] = 1
    'add blockers, 2 = uni, 4 = omni'
    for block in range(20):
        for block2 in range(20):
            active[time2][block+13][5+block2] = 2

'loop through time'
for timee in tqdm(range(pointTotal)):
    'loop down grid'
    for i in range(0, gridSize):
        'loop across grid'
        for j in range(0,gridSize):
            'define cell object'
            cell = Grid(timee,i,j,heart,active,gridSize,threshold,pointTotal,0,diffuse,sampleRate)
            'call gridchange function on cell'
            cell.gridChange()
            'if s_t values got, do calc, if not, skip'
            if cell.skip > 0:
                'define time period for differential equation using length of s_t'
                t2  = np.linspace(0, len(cell.s_t)-1, len(cell.s_t))
                'define differential equation and solve'
                AP2 = DE(0.15, 2.5, 0.01, 0.06, 0 , 0, t2, cell.s_t)
                AP2.Solve2()
                cell2 = Grid(timee,i,j,heart,active,gridSize,threshold,pointTotal,AP2.u,diffuse,sampleRate)
                'if up and down reference do pulsechange '
                if cell.skip == 1:
                    cell2.pulseChange()
    'end simulation earlier to avoid time boundary issues'
    if timee > (pointTotal - 100):
        break
np.save('heart', heart)
