import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit


class EstimationProblem():
    """
    Base class for the parameter estimation. 
    
    Attributes
    ----------
    t : array(k)
        sample times
    Y : array(n,k)
        sample values in row form
    system : function(t,y,**args) -> array(n)
        derivative function. Must outupt an array(n)
    y0 : array(n)
        initial conditions, optional. Taken as `Y[:,0]` if not given.
    ivp_kwargs : 
        keyword arguments passed to `scipy.integrate.solve_ivp`.
    fitted : bool
        whether the problem has been fitted or not. 
    
    If fitted this is true, the following are defined also:
    
    parameters : array
        the best-fit parameters found for the system.
    parameter_errors: 
        the 95% confidence interval errors for the fitted parameters.
        
    Methods
    -------
    fit(initial_parameters,**curve_fit_kwargs)
        attempts to find the optimal parameters starting from `initial_parameters`
    
    output(t_eval)
        evaluates the fitted model on the given time array.
    """
    def __init__(self,t,Y,system,y0=None,**ivp_kwargs):
        """
        Parameters
        ----------
        
        """
        self.t = t
        self.Y = Y
        if y0 is None:
            self.y0 = Y[:,0]
        else:
            self.y0 = y0
        self.system = system
        self._dim = len(self.y0)
        self._scale = Y.ptp(axis=1)[:,None]
        self.ivp_kwargs = ivp_kwargs
        self.fitted = False
        self._p = 0.0
        self._pcov = 0.0
        self._results = {}
    def __repr__(self):
        prefix = "un"*self.fitted + "fitted"
        return f"<{prefix} EstimationProblem with {self._dim} variables and {len(self.t)} samples>"
    
    @property
    def _flat_time(self):
        return np.ravel([i*self.t.max()+self.t for i in range(self._dim)])
    
    @property
    def parameters(self):
        if self.fitted:
            return self._p
        else:
            raise RuntimeError("System has not been fitted yet")
            
    @property
    def parameter_errors(self):
        if self.fitted:
            return 1.644853*np.sqrt(np.diag(self._pcov))
        else:
            raise RuntimeError("System has not been fitted yet")
    
    def __normalize(self,X):
        return np.ravel(X/self._scale)
    
    def __simulate(self,time, *params, normalize=True):
        time = time[:len(time)//self._dim]
        sol = solve_ivp(
            fun=self.system,
            y0=self.y0,
            t_span=(min(time),max(time)),
            t_eval=time,
            args=params,
            **self.ivp_kwargs
        )
        return self.__normalize(sol.y) if normalize else sol.y
    
    def fit(self,initial_parameters,**curve_fit_kwargs):
        try:
            p,cov,info,mesg,iters = curve_fit(
                self.__simulate,
                self._flat_time,
                self.__normalize(self.Y),
                p0=initial_parameters,
                full_output=True,
                **curve_fit_kwargs
            )
            self._p = p
            self._pcov = cov
            self._results = info
            self.fitted = True
            return mesg
        except ValueError:
            raise ValueError("Bad initial parameters?")
            
    def output(self,t_eval):
        "evaluates the fitted model on the given time array."
        return self.__simulate(
            np.concatenate([t_eval for i in range(self._dim)]),
            *self.parameters,
            normalize=False
        )