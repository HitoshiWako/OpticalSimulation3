import numpy as np

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
        return np.abs((eta0*param[0]-param[1])/(eta0*param[0]+param[1]))**2
    return tuple(map(_reflectance,param,eta0))

def calc_matrix(layers,n0,angle,lam):
    mat = (np.eye(2),np.eye(2))
    for layer in layers:
        mat = tuple(map(lambda m1,m2:np.dot(m1,m2),mat,characteristic_matrix(layer[lam],layer['d'],n0[lam],angle,lam)))
    return mat

def transmittance(param,eta0,eta_s):
    def _transmittance(param,eta0,eta_s):
        return 4*eta0*eta_s.real/np.abs(eta0*param[0]+param[1])**2
    return tuple(map(_transmittance, param, eta0,eta_s))