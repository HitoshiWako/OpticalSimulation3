import requests
import numpy as np

from sqlalchemy.orm import sessionmaker
from scipy import interpolate

from .settings import Engine
from .models import Material, OpticalIndex

Session = sessionmaker(bind=Engine)

def add_opticalindex(url):
    response = requests.get(url)
    if response.status_code == 200:
        
        name = url.split('/')[-1]
        text = response.text
        
        session = Session()

        material = session.query(Material).filter_by(name=name).one_or_none()
        if material is None:
            material = Material(name=name)
            session.add(material)
            material = session.query(Material).filter_by(name=name).one()
            lines = text.splitlines()
            lines.pop(0)
            opticalindexes = [OpticalIndex(material_id=material.id,wavelength=line.split()[0],
                                           n=line.split()[1],k=line.split()[2]) for line in lines]
            session.add_all(opticalindexes)
            session.commit()
        session.close()
    return response.status_code

def get_material_list():
    session = Session()
    qs = session.query(Material).all()
    session.close()
    return [(q.id,q.name) for q in qs]

def get_material_name(id):
    session = Session()
    q = session.query(Material).filter_by(id=id).one_or_none()
    return q.name

def get_opticalindex(id):
    session = Session()
    qs = session.query(OpticalIndex).filter_by(material_id=id).order_by(OpticalIndex.wavelength).all()
    session.close()
    ws = [q.wavelength for q in qs]
    nks = [complex(q.n,-q.k) for q in qs]
    return [ws,nks]

def fitted_opticalindex(id,start,end,step):    
    session = Session()
    qs = session.query(OpticalIndex).filter_by(material_id=id).order_by(OpticalIndex.wavelength).all()
    session.close()
    if len(qs) > 1:
        ws = [q.wavelength for q in qs]
        if ws[0] <= start and ws[-1] >= end:
            ns = [q.n for q in qs]
            ks = [q.k for q in qs]
            n_fitted = interpolate.interp1d(ws,ns)
            k_fitted = interpolate.interp1d(ws,ks)
            x = np.arange(start,end,step)
            return [complex(n,-k) for n,k in zip(n_fitted(x),k_fitted(x))]
    return []

def delete_opticalindex(id):
    Session = sessionmaker(bind=Engine)
    session = Session()
    q = session.query(Material).filter_by(id=id).one_or_none()
    if q is not None:
        session.query(OpticalIndex).filter_by(material_id=q.id).delete()
        session.delete(q)
        session.commit()
    session.close()

