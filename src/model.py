from sqlalchemy import (
    func,
    ForeignKey,
    Column,
    Integer,
    Float,
    String,
    text,
    DATE,
    DATETIME,
    exc
)
from src.extensions import db


class BaseModel(object):
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            sentry.captureException()
            return False

    def __get_value(self, key):
        if 'fecha' in key or 'hora' in key:
            return str(getattr(self, key))
        else:
            import decimal
            if isinstance(getattr(self, key), decimal.Decimal):
                return float(getattr(self, key))
            elif isinstance(getattr(self, key), bool):
                return int(getattr(self, key))
            else:
                return getattr(self, key)

    def to_dict(self):
        from sqlalchemy import inspect
        return {c.key: self.__get_value(c.key)
                for c in inspect(self).mapper.column_attrs}


class LocationRecord(db.Model, BaseModel):
    __tablename__ = 'historial_ubicaciones'
    __table_args__ = {'implicit_returning': False}
    id_historial_hubicacion = Column(Integer, primary_key=True, nullable=False)
    id_ruta = Column(Integer)
    fecha_registro = Column(String(10))
    kilometrage_dia = Column(Float)
    km_calculo = Column(Integer)

    def __init__(self, id_ruta, fecha_registro, kilometrage_dia, km_calculo):
        self.id_ruta = id_ruta
        self.fecha_registro = fecha_registro
        self.kilometrage_dia = kilometrage_dia
        self.km_calculo = km_calculo

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class DetailLocationRecord(db.Model, BaseModel):
    __tablename__ = 'historial_ubicaciones_detalle'
    __table_args__ = {'implicit_returning': False}
    id_historial_hubicacion_detalle = Column(Integer, primary_key=True, nullable=False)
    id_historial_hubicacion = Column(String(5))
    latitud = Column(String(30))
    longitud = Column(String(30))
    velocidad = Column(Float)
    fecha = Column(DATE)
    hora = Column(DATETIME())
    orden = Column(Integer)

    def __init__(self, id_historial_hubicacion, latitud, longitud, velocidad, fecha, hora, orden):
        self.id_historial_hubicacion = id_historial_hubicacion
        self.latitud = latitud
        self.longitud = longitud
        self.velocidad = velocidad
        self.fecha = fecha
        self.hora = hora
        self.orden = orden

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


