import matplotlib.pyplot as plt
import random
import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib.widgets import Slider, Button

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

#set to the parameters of the calculated output
t = 600
Y = 81
X = 81
T0 = int(t/10)

#import binary file
datafile = np.load('heart.npy')
Tint = datafile[T0,:,:]

#generate heatmap
heatmap = plt.imshow(Tint, cmap='plasma', interpolation='nearest')
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('temp')

#create time variable slider
axTime = plt.axes([0.25, 0.1, 0.65, 0.03])
sTime = Slider(axTime, 'Time', 0, t-1, valinit=T0, valfmt='%0.0f')

def update(val):
    Time = int(sTime.val)
    ti = datafile[Time,:,:]
    heatmap.set_data(ti)
sTime.on_changed(update)

axreset = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(axreset, 'Reset')

def reset(event):
    sTime.reset()
button.on_clicked(reset)


plt.show()
