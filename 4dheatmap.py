import matplotlib.pyplot as plt
import random
import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib.widgets import Slider, Button

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

#set parameters of the binary file
Z = 10
Y = 10
X = 10
T = 200
D0 = int(Z/2)
T0 = 0

#load binary file
datafile = np.load('heart.npy')

z0 = datafile[T0,:,:,D0]

#generate heatmap
heatmap = plt.imshow(z0, cmap='magma', interpolation='bicubic')
plt.clim(-1,2)
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('')

#create time and depth sliders
axtime = plt.axes([0.25, 0.13, 0.65, 0.03])
axdepth = plt.axes([0.25, 0.08, 0.65, 0.03])
sdepth = Slider(axdepth, 'Depth', 0, Z-1, valinit=D0, valfmt='%0.0f')
stime = Slider(axtime, 'Time', 0, T-1, valinit=T0, valfmt='%0.0f')

def update(val):
    depth = int(sdepth.val)
    time = int(stime.val)
    zi = datafile[time,:,:,depth]
    heatmap.set_data(zi)
sdepth.on_changed(update)
stime.on_changed(update)

axreset = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(axreset, 'Reset')

def reset(event):
    sdepth.reset()
    stime.reset()
button.on_clicked(reset)

plt.show()
