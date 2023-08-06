import numpy as np

def decay(t,Y,*args):
    """Simple radioactive decay with parameter
    λ = reciprocal of the mean lifetime.
    """
    λ, = args
    N, = Y
    return -λ*N
def housekeeping(t,Y,*args):
    """Housekeeping gene expression from mRNA to protein,
    with constants km,γm,kp,γp; k being creation and γ degradation.\n
    The variables are (m,p)."""
    km,γm,kp,γp = args
    m,p = Y
    return np.array([
        km - m*γm,
        kp*m - γp*p
    ])
def lotka_volterra(t,Y,*args):
    """predator, prey dynamics with parameters:
    * α: prey birth rate
    * β: predator efficiency on consuming prey
    * γ: predator famine
    * δ: predator birth rate\n
    The variables are (prey,predator)
    """
    α,β,γ,δ = args 
    x,y = Y
    return np.array([
        α*x - β*x*y,
        δ*x*y - γ*y 
    ])
def SIR(t,Y,*args):
    """Susceptible-Infected-Removed epidemiology model, with parameters:
    * N: total population
    * β: inverse of the typical time between contacts
    * γ: inverse of typical time until removal\n
    The variables are (S,I,R)
    """
    N,β,γ = args
    S,I,R = Y
    return np.array([
        -β*I*S/N,
        β*I*S/N-γ*I,
        γ*I
    ])
def damped_coupled_oscillator(t,Y,*args):
    """A pair of oscillators of the same mass, 
    one attached to a wall, the other attached to the one.\n
    The parameters are ω1,γ1,ω2,γ2, with ω the natural 
    frecuencies and γ the damping.\n 
    The variables are x1,v1,x2,v2
    """
    ω1,γ1,ω2,γ2 = args
    x1,v1,x2,v2 = Y 
    return np.array([
        v1, # dx1
        - γ1*v1 - ω1**2*x1 - ω2**2*(x1-x2), # dv1
        v2, # dx2
        - γ2*v2 + ω2**2*(x1-x2) # dv2
    ])
def lorenz_fetter(t,Y,*args):
    """Lorenz-Fetter-Hamilton chaotic oscillator 
    for atmospheric convection with parameters:
    * σ: Prandtl number
    * ρ: Rayleigh number
    * β: atmospheric depth\n
    The variables are:
    * x: rate of convection
    * y: horizontal temperature variation
    * z: vertical temperature variation
    """
    σ,ρ,β = args
    x,y,z = Y
    return np.array([
        σ*(y-x),
        x*(ρ-z)-y,
        x*y-β*z
    ])

systems = {
    "Radioctive decay":{
        "fun": decay,
        "t_span": (0,10),
        "params": [np.log(2)],
        "ini": [0.5],
        "dim": 1,
        "vars": "N"
    },
    "Housekeeping gene expression":{
        "fun": housekeeping,
        "t_span": (0,100),
        "params": [1, 1/5, 30, 1/50],
        "ini": [2, 0.1, 2, 0.1],
        "dim": 2,
        "vars": ["mRNA","protein"]
    },
    "Lotka-Volterra":{
        "fun": lotka_volterra,
        "t_span": (0,10),
        "params": [1.5, 4.2, 3.15, 7.0 ],
        "ini": [1.4,4,3,7.2],
        "dim": 2,
        "vars": ["prey","predator"]
    },
    "SIR epidemics":{
        "fun": SIR,
        "t_span": (0,10),
        "params": [ 3, 3, 0.3 ],
        "ini": [1.0, 1.0, 1.0],
        "dim": 3,
        "vars": ["S","I","R"]
    },
    "Damped coupled oscillators":{
        "fun": damped_coupled_oscillator,
        "t_span": (0,10),
        "params": [3.5,0.8,4.2,1.1],
        "ini": [1,1,1,1],
        "dim": 4,
        "vars": ["$x_1$","$v_1$","$x_2$","$v_2$"]
    },
    "Lorenz-Fetter-Hamilton oscillator":{
        "fun":lorenz_fetter,
        "t_span": (0,2),
        "params": [10,20,8/3],
        "ini": [9,18,2.5],
        "dim": 3,
        "vars": ["x","y","z"]
    }
}