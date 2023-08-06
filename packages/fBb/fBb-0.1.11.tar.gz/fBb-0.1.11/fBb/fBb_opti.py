#!/usr/bin/env python3

"""
An open source package to interpolate time series by multipoint fractional Brownian bridges 
url="https://github.com/fiddir/fBb"
license="MIT license"
"""

import numpy as np
from stochastic.processes.continuous import FractionalBrownianMotion

class MFBB:
    def __init__(self, X_i, t_i, H, N_fine, sigma=None): 
        self.X_i = X_i
        self.t_i = t_i
        self.H = H
        self.N_fine = N_fine
        self.N_coarse = np.size(X_i)
        #if sigma is None:
        #    self.X_i /= np.std(self.X_i)#*np.sqrt(2)
        #    self.sigma = 1.
        #    #self.X_i -= np.mean(self.X_i)
        #    #self.sigma = np.std(self.X_i)/self.t_i[-1]**self.H
        #else:
        #    self.sigma = sigma
        self.sigma = 1.
        fbm = FractionalBrownianMotion(hurst=self.H, t=self.t_i[-1])
        phases = np.fft.rfft(np.random.normal(0, 1, self.N_fine))
        dt = t_i[-1]/self.N_fine
        self.t = np.arange(self.N_fine+1)*dt
        self.omega = np.arange(self.N_fine//2+1)/(N_fine//2+1)*2*np.pi/t_i[-1]
        hat_X = self.omega**(-1./2.-H)*phases
        hat_X[self.omega==0] = 0.
        self.X = np.fft.irfft(hat_X)
        self.X = self.sigma*self.X
        self.t = fbm.times(self.N_fine)
        #self.t_i = self.t[::self.N_fine//self.N_coarse]
        
    def cov(self, t, t_prime):
        T, T_prime = np.meshgrid(t, t_prime)
        return self.sigma**2*(T**(2*self.H)+T_prime**(2*self.H)-np.abs(T-T_prime)**(2*self.H))/2.
    
    def bridge(self):
        coarse_points  = np.arange(1,self.N_coarse+1)*self.N_fine//self.N_coarse
        X_bridge = self.X - (self.X[coarse_points]-self.X_i)@np.linalg.inv(self.cov(self.t_i,self.t_i))@self.cov(self.t, self.t_i)
        return X_bridge
    
    def free(self):
        return self.X
        
    def t_fine(self):
        return self.t
    
    def t_coarse(self):
        return self.t_i

def s_2(X_bridge):
    N_fine = np.size(X_bridge)
    struc = np.zeros(N_fine//2)
    tau_sample = np.arange(1, N_fine//2+1)
    for rr in range(1, N_fine//2+1):
        struc[rr-1] = np.var(X_bridge[:-rr]-X_bridge[rr::])
    return tau_sample, struc
    #def hurst(self):
    #    return self.bridge()

def optimal(H, t_i, X_i, N_fine):
    realizations = 40
    N_coarse = np.size(X_i)
    mfbb = MFBB(X_i, t_i, H, N_fine)
    struc_ave = np.zeros(N_fine//2)
    for nn in range(realizations):
        X_bridge = mfbb.bridge()
        tau, struc = s_2(X_bridge)
        struc_ave += struc/realizations 
    p, res , _, _, _ =  np.polyfit(np.log(tau[:N_fine//N_coarse]), np.log(struc_ave[:N_fine//N_coarse]),1, full=True)
    H_est = p[0]/2.
    lstq = res[0]
    print( np.abs(H_est-H), lstq) 
    return np.abs(H_est-H), lstq

def optimal_hurst(t_i, X_i, N_fine, N_hurst):
    H = np.linspace(0.1, 0.8, N_hurst)
    lstq_H = np.zeros(N_hurst)
    opti_H = np.zeros(N_hurst)
    for hh in range(N_hurst):
        opti_H[hh], lstq_H[hh] = optimal(H[hh], t_i, X_i, N_fine)
    return opti_H, lstq_H


