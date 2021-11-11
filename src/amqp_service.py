from nameko.rpc import rpc, RpcProxy
from functional import seq
from sqlalchemy import exc
from src.service import PointService
from src.extensions import db


class AmqpService:
    name = 'amqp_services'

    def __init__(self):
        self.point_service = PointService()


    def create_location_detail(self,point, index, location_id):
        args = {
            'id_historial_hubicacion': location_id,
            'latitud': point['latitud'],
            'longitud': point['longitud'],
            'velocidad': point['velocidad'],
            'fecha': point['fecha'],
            'hora': point['hora'],
            'orden': index
        }
        detail = self.point_service.create_detail(**args)
        return detail

    @rpc
    def append_identifier(self, value):
        print('entro aqui {}-y'.formtat(value))
        return u"{}-y".format(value)

    @rpc
    def insert_travel(self, id_route: int, date: str, points: list):
        from app import app
        db.app = app
        print(db)
        exits_locations = False
        try:
            location = self.point_service.get_location(id_route, date)
            #self.point_storage.storage(routes, name, 'locations')
            if location:
                location_id = location.id_historial_hubicacion
                rows = self.point_service.get_total_rows(location_id)
                exits_locations = True
            else:
                new_location = self.point_service.create(id_ruta=id_route,
                                                         fecha_registro=date,
                                                         kilometrage_dia=0,
                                                         km_calculo=0)
                if not new_location:
                    return {'data': None, 'message': 'Ocurrio un error al insertar'}, 400
                location_id = new_location.id_historial_hubicacion

            points = seq(points) \
                .map(lambda point: self.create_location_detail(point, points.index(point) + 1 if not exits_locations else points.index(point) + rows, location_id)).to_list()

            db.session.add_all(points)
            db.session.commit()
            print('Travel inserted successfully!')
            return 1
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error {str(e)}")
            return {'message': 'Ocurrio un error al insertar recorrido'}, 400
    