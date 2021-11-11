from sqlalchemy import VARCHAR, TIME, func, and_, cast, String, Float
from sqlalchemy.sql import bindparam
from functional import seq
from src.model import (
    LocationRecord,
    DetailLocationRecord
)
from src.extensions import db


class PointService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def create(self, **kwargs):
        location = LocationRecord(**kwargs)
        return location if location.save() else None

    def update_distance(self, pk_location, distance):
        location = LocationRecord.query.get(pk_location)
        setattr(location, 'kilometrage_dia', distance + location.kilometrage_dia)
        setattr(location, 'km_calculo', 1)
        db.session.commit()
        return location

    def create_detail(self, **kwargs):
        detail = DetailLocationRecord(**kwargs)
        return detail

    def get_location(self, pk_route, date):
        location = LocationRecord.query.filter(
            LocationRecord.id_ruta == pk_route, LocationRecord.fecha_registro == date
        ).first()
        return location if location else None

    def get_total_rows(self, pk_location):
        rows = db.session \
            .query(DetailLocationRecord.id_historial_hubicacion_detalle) \
            .filter(DetailLocationRecord.id_historial_hubicacion == pk_location) \
            .count()
        return rows+1 if rows else 0

    def delete(self, pk):
        location = LocationRecord.query.get(pk)
        db.session.delete(LocationRecord.query.get(pk))
        db.session.commit()
        return location

    def delete_detail(self, pk_location):
        try:
            db.session \
                .query(DetailLocationRecord) \
                .filter(DetailLocationRecord.id_historial_hubicacion == pk_location).delete()
            return True
        except:
            return False


    def measure_distance(self, before_point, current_point):
        previous_place = (before_point['latitud'], before_point['longitud'])
        current_place = (current_point['latitud'], current_point['longitud'])
        distance = geodesic(previous_place, current_place)
        return {'distance': distance.kilometers}

    def add_all_travel(self, points):
        try:
            db.session.add_all(points)
            db.session.commit()
            return True
        except Exception as e:
            return False
            db.session.rollback()
            sentry.captureException()
