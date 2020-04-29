import numpy as np
'set size of grid'
gridSize = 41
'set diffuse time, minimum one iteration'
diffuse = 1
'set number of time steps to simulate over'
modelLength = 300
'set how many iterations per time step. Increasing this'
'will naturally decrease diffusion time'
sampleRate = 4
'set value to detect for threshold voltage'
threshold = 0.01
'calculate number of total iterations'
pointTotal = modelLength * sampleRate
t  = np.linspace(0, modelLength, pointTotal)
t2  = np.linspace(0, 10, 10)
