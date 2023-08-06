from sqlalchemy import Column, DateTime, Numeric, Integer, String, Date
from .base import Base

class ArbaPadronGeneralPercepciones(Base):
    """ Arba Padron General Percepciones """
    
    __tablename__ = "arba_padron_general_percepciones"
    __table_args__ = ({"postgresql_partition_by": "LIST (periodo)"},)
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    periodo = Column(String(6), primary_key=True)
    fecha_publicacion = Column(Date, nullable=False)
    fecha_vigencia_desde = Column(Date, nullable=False)
    fecha_vigencia_hasta = Column(Date, nullable=False)
    cuit = Column(String(11), nullable=False)
    tipo_contr_insc = Column(String(1))
    marca_alta_sujeto = Column(String(1))
    marca_cambio_alicuota = Column(String(1))
    alicuota = Column(Numeric(5,2), nullable=False)
    nro_grupo = Column(Numeric(2,0))

class ArbaPadronGeneralRetenciones(Base):
    """ Arba Padron General Retenciones """
    
    __tablename__ = "arba_padron_general_retenciones"
    __table_args__ = ({"postgresql_partition_by": "LIST (periodo)"},)
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    periodo = Column(String(6), primary_key=True)
    fecha_publicacion = Column(Date, nullable=False)
    fecha_vigencia_desde = Column(Date, nullable=False)
    fecha_vigencia_hasta = Column(Date, nullable=False)
    cuit = Column(String(11), nullable=False)
    tipo_contr_insc = Column(String(1))
    marca_alta_sujeto = Column(String(1))
    marca_cambio_alicuota = Column(String(1))
    alicuota = Column(Numeric(5,2), nullable=False)
    nro_grupo = Column(Numeric(2,0))

class DescargaPadronesHistory(Base):
    """ Histórico de descarga de padrones """
    
    __tablename__ = "descarga_padrones_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    padron = Column(String(100), nullable=False)
    periodo = Column(String(6), nullable=True)

class AgipPadronGeneral(Base):
    """Agip Padron General"""

    __tablename__ = "agip_padron_general"
    __table_args__ = ({"postgresql_partition_by": "LIST (periodo)"},)
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    periodo = Column(String(6), primary_key=True)
    fecha_publicacion = Column(Date, nullable=False)
    fecha_vigencia_desde = Column(Date, nullable=False)
    fecha_vigencia_hasta = Column(Date, nullable=False)
    cuit = Column(String(11), nullable=False)
    tipo_contr_insc = Column(String(1))
    marca_alta_sujeto = Column(String(1))
    marca_alicuota = Column(String(1))
    alicuota_percepcion = Column(Numeric(5,2), nullable=False)
    alicuota_retencion = Column(Numeric(5,2), nullable=False)
    nro_grupo_percepcion = Column(String(2))
    nro_grupo_retencion = Column(String(2))
    razon_social = Column(String(60))
