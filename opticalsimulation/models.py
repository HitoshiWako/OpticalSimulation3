from sqlalchemy import Column, Integer, Float, String

from opticalsimulation.settings import Base

class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Material(name={})>".format(
            self.name,
        )

class OpticalIndex(Base):
    __tablename__ = 'opticalindex'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer)
    wavelength = Column(Float)
    n = Column(Float)
    k = Column(Float)

    def __repr__(self):
        return "<Optical Index(material id={}, wavelength={}, n={}, k={})>".format(
            self.material_id,
            self.wavelength,
            self.n,
            self.k
        )