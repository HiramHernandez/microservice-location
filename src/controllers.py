import json
from flask_restful import Resource, request
from sqlalchemy import exc
from functional import seq
from src.service import PointService
from src.amqp_service import AmqpService
from nameko.standalone.rpc import ClusterRpcProxy

def create_location_detail(point, index, location_id):
    poit_service = PointService()
    args = {
        'id_historial_hubicacion': location_id,
        'latitud': point['latitud'],
        'longitud': point['longitud'],
        'velocidad': point['velocidad'],
        'fecha': point['fecha'],
        'hora': point['hora'],
        'orden': index
    }
    detail = poit_service.create_detail(**args)
    return detail

CONFIG = {'AMQP_URI': 'amqp://guest:guest@192.168.99.100'}

class PointsListController(Resource):
    def __init__(self, *args, **kwargs):
        #self.route_service = RouteService()
        #self.point_storage = StorageBody()
        self.point_service = PointService()
        self.amqp_service = AmqpService()

    def get(self):
        operation = 'sum'
        value = 10
        other = 234
        email =  "hhg.mzt@gmail.com",
        msg = "Please wait the calculation, you'll receive an email with results"
        subject = "API Notification"
        with ClusterRpcProxy(CONFIG) as rpc:
            # asynchronously spawning and email notification
            rpc.mail.send.call_async(email, subject, msg)
            # asynchronously spawning the compute task
            result = rpc.compute.compute.call_async(operation, value, other, email)
            return msg, 200

    def post(self):
        routes = json.loads(request.data.decode("utf-8"))
        id_route = routes['root']['id_ruta']
        points = routes['root']['points']
        date = routes['root']['fecha']
        msg = 'Please wait for insert travel'

        with ClusterRpcProxy(CONFIG) as rpc:
            result = rpc.amqp_services.insert_travel.call_async(id_route, date, points)
            #result = rpc.amqp_service.append_identifier(22)
            return msg, 200


    def put(self):
        routes = json.loads(request.data.decode("utf-8"))
        id_route = routes['root']['id_ruta']
        points = routes['root']['points']
        date = routes['root']['fecha']
        #name = self.route_service.get_name_by_pk(id_route)
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
                .map(lambda point: create_location_detail(
                    point, points.index(point) + 1 if not exits_locations else points.index(point) + rows, location_id)).to_list()

            db.session.add_all(points)
            db.session.commit()

            #self.point_service.calculate_travel(id_route, date, location_id)
            return {'data': location.to_dict() if exits_locations else new_location.to_dict(),
                    'message': 'El recorrido se registro satisfactoriamente'}, 201
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error {str(e)}")
            return {'message': 'Ocurrio un error al insertar recorrido'}, 400

