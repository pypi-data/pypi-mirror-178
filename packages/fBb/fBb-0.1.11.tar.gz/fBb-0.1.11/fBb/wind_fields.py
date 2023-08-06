#!/usr/bin/env python3

"""
An open source package to generate synthetic wind fields
url="https://github.com/fiddir/superstat_WIND"
license="MIT license"
"""

import matplotlib                                                                                                                                                                                                                                                                                                                                               
import numpy as np
import math                                                                                                                                                                                                                                                                                                                                                   
import scipy.stats as stats
import scipy                                                                                                                                                                                                                                                                                                                                        
import scipy.special as sc
from scipy.special import gamma, factorial
import scipy.special as sc

class SWF:
    def __init__(self, H, mu, L, tilde_L, eta, dx, N_x, N_y, N_z, sigma=None): 
        self.H = H
        self.mu = mu
        self.L = L
        self.tilde_L = tilde_L
        self.eta = eta
        self.dx = dx
        self.N_x = N_x
        self.N_y = N_y
        self.N_z = N_z
        if sigma is None:
             self.sigma = 1. 
        else:
            self.sigma = sigma
        x = np.linspace(0, self.dx*(self.N_x/2-1), self.N_x//2)
        x = np.append(x, x[::-1])
        y = np.linspace(0, self.dx*(self.N_y/2-1), self.N_y//2)
        y = np.append(y, y[::-1])
        z = np.linspace(0, self.dx*(self.N_z/2-1), self.N_z//2)
        z = np.append(z, z[::-1])
        #x = np.append(np.append(np.append(x,x),x),x)                                                                                                                                                                                                                                                                                                                             
        R_X, R_Y, R_Z = np.meshgrid(x, y, z, indexing='ij')
        self.R = np.sqrt(R_X**2+R_Y**2+R_Z**2)
        kx = np.linspace(-self.N_x//2, self.N_x//2-1, self.N_x)
        ky = np.linspace(-self.N_y//2, self.N_y//2-1, self.N_y)
        kz = np.linspace(0, self.N_z//2, self.N_z//2+1)
        self.KX, self.KY, self.KZ = np.meshgrid(kx, ky, kz, indexing='ij')
        K2 =  np.square(self.KX)+np.square(self.KY)+np.square(self.KZ)
        self.K = np.sqrt(K2)
        print(self.K.shape, self.R.shape)

    
    def fou(self, lam):
        A = 0.
        R = np.abs(self.R)
        r = np.where(R+self.eta>=self.tilde_L,((R+self.eta)/self.tilde_L)**(self.mu/2)*R, lam**np.sqrt(A+self.mu*np.log(self.tilde_L/(R+self.eta)))*((R+self.eta)/self.tilde_L)**(self.mu/2)*R)
        return self.sigma**2*self.L**(2*self.H)/4.*(2*np.cosh(r/self.L)*gamma(2*self.H+1)+np.exp(-r/self.L)*(r/self.L)**(2*self.H+1)/(2*self.H+1)*sc.hyp1f1(2*self.H+1, 2*self.H+2, r/self.L) \
               -np.exp(r/self.L)*(r/self.L)**(2*self.H+1)/(2*self.H+1)*sc.hyp1f1(2*self.H+1, 2*self.H+2, -r/self.L))-self.sigma**2*r**(2*self.H)/2.

    def field(self):
        N_xi = 60#600                                                                                                                                                                                                                                                                                                                                                             

        random_phases = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        u_field = np.zeros((N_xi, self.N_x, self.N_y, self.N_z))
        lam_array = np.sort(np.random.lognormal(0, 1, N_xi))
        
        for nn in range(N_xi):
            lam = lam_array[nn]                                                                                                                                                                                                                                                                                                                                                          
            corr_ou = self.fou(lam)
            hat_corr_ou = np.fft.fftshift(np.fft.rfftn(corr_ou),axes=(0,1))
            amplitudes = np.sqrt(hat_corr_ou)
            amplitudes[self.KX==0] *= np.exp(-self.K[self.KX==0]**2*0.01)
            amplitudes[self.KY==0] *= np.exp(-self.K[self.KY==0]**2*0.01)
            amplitudes[self.KZ==0] *= np.exp(-self.K[self.KZ==0]**2*0.01)
            hat_u = amplitudes*random_phases
            u_field[nn] = np.fft.irfftn(np.fft.ifftshift(hat_u,axes=(0,1)))
        y = np.random.randn(N_x)
        T = 2.
        z_hat = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        v= np.zeros((self.N_x, self.N_y, self.N_z))
        corr_ou = self.fou(1.)
#corr_ou = np.append(corr_ou, corr_ou[::-1])
        hat_corr_ou = np.fft.fftshift(np.fft.rfftn(corr_ou), axes=[0,1])
        amplitudes = np.sqrt((hat_corr_ou))
        amplitudes[self.KX==0] *= np.exp(-self.K[self.KX==0]**2*0.01)
        amplitudes[self.KY==0] *= np.exp(-self.K[self.KY==0]**2*0.01)
        amplitudes[self.KZ==0] *= np.exp(-self.K[self.KZ==0]**2*0.01)
        z_hat *= amplitudes
        z_hat[self.K==0] = 0.
        y = np.fft.irfftn(np.fft.ifftshift(z_hat,axes=(0,1)))
        y /= np.std(y)
        y = 1./2*(1+sc.erf(y/np.sqrt(2)))
#plt.plot(z)                                                                                             
        y -= y.min()
        y /= y.max()
        y *= (N_xi-1)
        y = y.astype(int)
#plt.imshow(z[:,:,10])                                                                                   
        for xx in range(self.N_x):
            for yy in range(self.N_y):
                for zz in range(self.N_z):
                    v[xx,yy,zz] = u_field[y[xx,yy,zz],xx,yy,zz]
        return v/np.std(v)


# wind field parameters
H=0.33; mu=0.22; L=1.1; tilde_L=1.1; N_x=128; N_y=128; N_z=128; dx=L/256.; eta=dx
swf = SWF(H, mu, L, tilde_L, eta, dx, N_x, N_y, N_z)
u = swf.field()
