import numpy as np
from copy import copy

Y0 = np.sqrt(8.8541878128/1.25663706212)*1e-3

def snell(n1,n0,theta):
    return np.arcsin(n0.real/n1.real*np.sin(theta))

def admittance(n1,n0,theta):
    phi = snell(n1,n0,theta)
    return (Y0*n1*np.cos(phi), Y0*n1/np.cos(phi))

def phasedifference(n,d,phi,lm):
    return 2*np.pi*n*d*np.cos(phi)/lm

def characteristic_matrix(n,d,n0,angle,lam):
    eta = admittance(n,n0,angle)
    phi = snell(n,n0,angle)
    delta = phasedifference(n,d,phi,lam)
    c = np.cos(delta)
    s = np.sin(delta)
    def _matrix(et):
        return (np.array([[c,1j*s/et],[1j*s*et,c]]))
    return tuple(map(_matrix, eta))

def reflectance(param, eta0):
    def _reflectance(param, eta0):
        return (np.abs((eta0*param[0]-param[1])/(eta0*param[0]+param[1]))**2)[0]
    return tuple(map(_reflectance,param,eta0))

# def calc_matrix(layers,n0,angle,lam):
#     mat = (np.eye(2),np.eye(2))
#     for layer in layers:
#         mat = tuple(map(lambda m1,m2:np.dot(m1,m2),mat,characteristic_matrix(layer[lam],layer['d'],n0[lam],angle,lam)))
#     return mat

def calc_matrix(ns,ds,n0,n1,theta,lam):
    length = len(lam)
    eta = admittance(n1,n0,theta)
    
    v_s = tuple([np.array([np.ones(length),eta[0]]),
                 np.array([np.ones(length),eta[1]])])
    
    mat = tuple([np.array([[np.ones(length),np.zeros(length)],[np.zeros(length),np.ones(length)]]),
                 np.array([[np.ones(length),np.zeros(length)],[np.zeros(length),np.ones(length)]])])
    for n,d in zip(ns,ds):
        m = characteristic_matrix(n, d, n0,theta,lam)
        mat = tuple([np.array([[mat[0][0,0]*m[0][0,0]+mat[0][0,1]*m[0][1,0], mat[0][0,0]*m[0][0,1]+mat[0][0,1]*m[0][1,1]],
                               [mat[0][1,0]*m[0][0,0]+mat[0][1,1]*m[0][1,0], mat[0][1,0]*m[0][0,1]+mat[0][1,1]*m[0][1,1]]]),
                     np.array([[mat[1][0,0]*m[1][0,0]+mat[1][0,1]*m[1][1,0], mat[1][0,0]*m[1][0,1]+mat[1][0,1]*m[1][1,1]],
                               [mat[1][1,0]*m[1][0,0]+mat[1][1,1]*m[1][1,0], mat[1][1,0]*m[1][0,1]+mat[1][1,1]*m[1][1,1]]])])

    param = tuple([np.array([[mat[0][0,0]*v_s[0][0]+mat[0][0,1]*v_s[0][1]],[mat[0][1,0]*v_s[0][0]+mat[0][1,1]*v_s[0][1]]]),
                   np.array([[mat[1][0,0]*v_s[1][0]+mat[1][0,1]*v_s[1][1]],[mat[1][1,0]*v_s[1][0]+mat[1][1,1]*v_s[1][1]]])])
    return param

def transmittance(param,eta0,eta_s):
    def _transmittance(param,eta0,eta_s):
        return (4*eta0*eta_s.real/np.abs(eta0*param[0]+param[1])**2)[0]
    return tuple(map(_transmittance, param, eta0,eta_s))

def absorb(n1,thickness,n0,theta,lam):
    phi = snell(n1,n0,theta)
    return np.exp(-8*np.pi*np.abs(n1.imag)*thickness*1000/(lam*np.cos(phi)))

def calc_spectra(n0,n1,n2,theta,front_ns,front_ds,back_ns,back_ds,t_sub, lam):
     f_ns = copy(front_ns)
     f_ds = copy(front_ds)
     b_ns = copy(back_ns)
     b_ds = copy(back_ds)
     
     phi1 = snell(n1,n0,theta)
     # phi2 = snell(n2,n0,theta)
    
     eta0 = admittance(n0,n0,theta)
     eta1 = admittance(n1,n0,theta)
     eta2 = admittance(n2,n0,theta)
     
     front_forward = calc_matrix(f_ns,f_ds,n0,n1,theta,lam)
     f_ns.reverse()
     f_ds.reverse()
     front_backward = calc_matrix(f_ns,f_ds,n1,n0,phi1,lam)
     
     # back_forward = calc_matrix(b_ns,b_ds,n2,n1,phi2,lam)
     b_ns.reverse()
     b_ds.reverse()
     back_backward = calc_matrix(b_ns,b_ds,n1,n2,phi1,lam)
     
     r01 = reflectance(front_forward,eta0)
     r10 = reflectance(front_backward,eta1)
     t01 = transmittance(front_forward,eta0,eta1)
     t10 = transmittance(front_backward,eta1,eta0)
     
     r12 = reflectance(back_backward,eta1)
     t12 = transmittance(back_backward,eta1,eta2) 


     beta = absorb(n1,t_sub,n0,theta,lam)

     r = ((r01[0]+ t01[0]*r12[0]*t10[0]*beta)/(1-r10[0]*r12[0]*beta), 
          (r01[1]+ t01[1]*r12[1]*t10[1]*beta)/(1-r10[1]*r12[1]*beta))
     t = (t01[0]*t12[0]*np.sqrt(beta)/(1-r10[0]*r12[0]*beta),
          t01[1]*t12[1]*np.sqrt(beta)/(1-r10[1]*r12[1]*beta))

     return (r01,t01,r,t)