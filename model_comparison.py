import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint

k1 = 0.5
k1b = 0.005
k2 = 0.0058
r = 2.0

def eq1(var,t):
    m = var[0]
    dm = k1b + k1/(1+r) - k2*m
    return dm

def eq2(var,t):
    m = var
    dm = k1b + (k1 + k1b*r)/(1+r) - k2*m
    return dm

time = np.linspace(0.0,100.0,1000)
inval = 1.0
y1 = odeint(eq1,inval,time)
y2 = odeint(eq2,inval,time)

line1, = plt.plot(time,y1,color='green', label='Textbook')
line2, = plt.plot(time,y2,color='red', label='CA Voigt')
plt.xlabel('time')
plt.ylabel('mRNA concentration')
plt.gcf().canvas.set_window_title('Model equations comparison')
plt.legend(handles=[line1, line2])
plt.show()
