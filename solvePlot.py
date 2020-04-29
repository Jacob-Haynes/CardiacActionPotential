import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
class DE(object):
    def __init__(self, a, b, eps, s, u0, v0,t,s_t):
        self.a = a
        self.b = b
        self.eps = eps
        self.s = s
        self.s_t = s_t
        self.u0 = u0
        self.v0 = v0
        self.t = t
        'f(y,t) is dy/dt, where y is a vector, y[0] and y[1]'
        'each one representing one of the coupled ODEs'
    def Solve(self):
        'solve for single pulse'
        def s(t):
            if t < 5:
                return 0.06
            else:
                return 0
        def f(y, t):
            'define ui as du/dt, define vi as dv/dt'
            ui = y[0]
            vi = y[1]
            'two FH equations'
            f0 = (ui*(ui-self.a)*(1-ui)) - vi + s(t)
            f1 = self.eps*(ui - (self.b*vi))
            return [f0, f1]
        'make initial condition s into vector'
        y0 = [self.u0, self.v0]
        'solve the DEs odeint(function, initial vector, timegrid)'
        soln = odeint(f, y0, self.t)
        'u is soln for y[0], v for y[1]'
        self.u = soln[:, 0]
        self.v = soln[:, 1]
    def Solve2(self):
        'solve for cells taking s(t) from neighbouring cells'
        def s(t):
            't is sampled in a weird way, need integer values to get s_t values'
            if type(self.s_t) is list:
                i = int(t)
                'sometimes i can go out of range, slight fix added here'
                if i >= len(self.t):
                    i = len(self.t)-1
                return self.s_t[i]
            else:
                return self.s_t
        def f(y, t):
            'define ui as du/dt, define vi as dv/dt'
            ui = y[0]
            vi = y[1]
            'two FH equations'
            f0 = (ui*(ui-self.a)*(1-ui)) - vi + s(t)
            f1 = self.eps*(ui - (self.b*vi))
            return [f0, f1]
        'make initial condition s into vector'
        y0 = [self.u0, self.v0]
        'solve the DEs odeint(function, initial vector, timegrid)'
        soln = odeint(f, y0, self.t)
        'u is soln for y[0], v for y[1]'
        self.u = soln[:, 0]
        self.v = soln[:, 1]
    def Plot(self):
        plt.ion()
        plt.rcParams['figure.figsize'] = 10, 8
        plt.figure()
        plt.plot(self.t, self.u, label='u')
        plt.plot(self.t, self.v, label='v')
        plt.xlabel('Dimensionless Time')
        plt.ylabel('Fitzhugh-Nagumo Variable')
        plt.grid()
        plt.show(block=True)
