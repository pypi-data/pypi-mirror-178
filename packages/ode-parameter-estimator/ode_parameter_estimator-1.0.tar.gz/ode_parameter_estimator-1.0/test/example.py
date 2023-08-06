import numpy as np
import matplotlib.pyplot as plt
from ode_parameter_estimator import EstimationProblem

def lorenz(t,Y,*args):
    σ,ρ,β = args
    x,y,z = Y
    return np.array([
        σ*(y-x),
        x*(ρ-z)-y,
        x*y-β*z
    ])
    
t,*Y = np.loadtxt("samples.dat",unpack=True)
Y = np.array(Y)
plt.plot(t,Y.T,"o",fillstyle='none')
plt.savefig("data.svg")

problem = EstimationProblem(t,Y,lorenz)
problem.fit([9,18,2.5])

ts = np.linspace(0,2,200)
Ys = problem.output(ts)

plt.plot(t,Y.T,"o",fillstyle='none')
plt.gca().set_prop_cycle(None) # reset color cycle
plt.plot(ts,Ys.T)
plt.savefig("fit.svg")