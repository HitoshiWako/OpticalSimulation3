import requests
from sqlalchemy.orm import sessionmaker
from .settings import Engine
from .models import Material, OpticalIndex

Session = sessionmaker(bind=Engine)

def add_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        
        name = url.split('/')[-1]
        text = response.text
        
#        Session = sessionmaker(bind=Engine)
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

def get_data(name):
#    Session = sessionmaker(bind=Engine)
    session = Session()
    opticalindexes = session.query(OpticalIndex).\
                             join(Material,OpticalIndex.material_id == Material.id).\
                             filter_by(name=name).order_by(OpticalIndex.wavelength).all()
    result = [(opticalindex.wavelength, complex(opticalindex.n,-opticalindex.k)) for opticalindex in opticalindexes]
    session.close()
    return result

def get_material_name():
#    Session = sessionmaker(bind=Engine)
    session = Session()
    qs = session.query(Material).all()
    session.close()
    return [q.name for q in qs]


def delete_data(name):
#    Session = sessionmaker(bind=Engine)
    session = Session()
    q = session.query(Material).filter_by(name=name).one_or_none()
    if q is not None:
        session.query(OpticalIndex).filter_by(material_id=q.id).delete()
        session.delete(q)
        session.commit()
    session.close()