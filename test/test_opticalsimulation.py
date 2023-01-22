import pytest
import numpy as np


from opticalsimulation.opticalsimulation import snell,admittance,phasedifference,characteristic_matrix,reflectance,calc_matrix,transmittance,Y0

@pytest.mark.parametrize(('n1','n0','angle','theta'),[
    (1.0,1.0,5*np.pi/180,5*np.pi/180),          #媒質の屈折率が同じなら出射角は入射角に等しい
    (1.0-0.01j,1.0,5*np.pi/180,5*np.pi/180),    #消衰係数があっても関係ない
    (2.0-0.01j,1.0,0.0,0.0),                    #入射角が0なら常に出射角も0
])
def test_snell(n1,n0,angle,theta):
    assert snell(n1,n0,angle) == theta

@pytest.mark.parametrize(('n1','n0','angle','eta'),[
    (1.0,1.0,0.0,(Y0,Y0))
])
def test_admittance(n1,n0,angle,eta):
    assert admittance(n1,n0,angle) == eta

@pytest.mark.parametrize(('n','d','delta','lm','pd'),[
    (2.0,125,0,500,np.pi)
])
def test_phasedifference(n,d,delta,lm,pd):
    assert phasedifference(n,d,delta,lm)==pd

@pytest.mark.parametrize(('n','d','n0','angle','lam','mat'),[
    (1.0,0.0,1.0,0.0,550,np.eye(2))
])
def test_characteristic_matrix(n,d,n0,angle,lam,mat):
    assert np.all(np.isclose(characteristic_matrix(n,d,n0,angle,lam),mat))

@pytest.mark.parametrize(('n','d','n0','n_sub','angle','lam','ref'),[
    (1.0,0,1.0,1.5,0.0,550,(0.04,0.04)),
    (1.0,100,1.0,1.5,0.0,550,(0.04,0.04)),
    (1.5,0,1.0,1.5,0.0,550,(0.04,0.04)),
    (1.5,100,1.0,1.5,0.0,550,(0.04,0.04)),

])
def test_reflectance(n,d,n0,n_sub,angle,lam,ref):

    mat = characteristic_matrix(n,d,n0,angle,lam)

    eta_sub= admittance(n_sub,n0,angle)
    vec = (np.array([[1],[eta_sub[0]]]),np.array([[1],[eta_sub[1]]]))
    param = tuple(map(lambda m,v:np.dot(m,v),mat,vec))

    eta0= admittance(n0,n0,angle)
    assert np.all(np.isclose(reflectance(param,eta0),ref))

@pytest.mark.parametrize(('layers','n0','n_sub','angle','lam','ref'),[
    ([],{550:1.0},{550:1.5},0.0,550,(0.04,0.04)),
    ([{'d':0, 550:1.0}],{550:1.0},{550:1.5},0.0,550,(0.04,0.04)),
    ([{'d':0, 550:1.5}],{550:1.0},{550:1.5},0.0,550,(0.04,0.04)),
    ([{'d':100, 550:1.0}],{550:1.0},{550:1.5},0.0,550,(0.04,0.04)),
    ([{'d':100, 550:1.5}],{550:1.0},{550:1.5},0.0,550,(0.04,0.04)),
    ([{'d':100, 550:1.0},{'d':100, 550:1.5}],{550:1.0},{550:1.5},0.0,550,(0.04,0.04)),
])
def test_calc_matrix(layers,n0,n_sub,angle,lam,ref):
    mat = calc_matrix(layers,n0,angle,lam)
    eta_sub = admittance(n_sub[lam],n0[lam],angle)
    
    vec = (np.array([[1],[eta_sub[0]]]),np.array([[1],[eta_sub[1]]]))
    param = tuple(map(lambda m,v:np.dot(m,v),mat,vec))

    eta0= admittance(n0[lam],n0[lam],angle)
    assert np.all(np.isclose(reflectance(param,eta0),ref))

@pytest.mark.parametrize(('layers','n0','n_sub','angle','lam','trans'),[
    ([],{550:1.0},{550:1.5},0.0,550,(0.96,0.96)),
    ([{'d':0, 550:1.0}],{550:1.0},{550:1.5},0.0,550,(0.96,0.96)),
    ([{'d':0, 550:1.5}],{550:1.0},{550:1.5},0.0,550,(0.96,0.96)),
    ([{'d':100, 550:1.0}],{550:1.0},{550:1.5},0.0,550,(0.96,0.96)),
    ([{'d':100, 550:1.5}],{550:1.0},{550:1.5},0.0,550,(0.96,0.96)),
    ([{'d':100, 550:1.0},{'d':100, 550:1.5}],{550:1.0},{550:1.5},0.0,550,(0.96,0.96)),
])
def test_transmittance(layers,n0,n_sub,angle,lam,trans):
    mat = calc_matrix(layers,n0,angle,lam)
    eta_sub = admittance(n_sub[lam],n0[lam],angle)
    
    vec = (np.array([[1],[eta_sub[0]]]),np.array([[1],[eta_sub[1]]]))
    param = tuple(map(lambda m,v:np.dot(m,v),mat,vec))

    eta0= admittance(n0[lam],n0[lam],angle)
    assert np.all(np.isclose(transmittance(param,eta0,eta_sub),trans))
