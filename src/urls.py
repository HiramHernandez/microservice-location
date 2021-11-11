from flask import Blueprint
from flask_restful import Api
from src.controllers import PointsListController

urls = Blueprint('urls', __name__)
api = Api(urls, prefix='/api/web')

api.add_resource(PointsListController, '/points')