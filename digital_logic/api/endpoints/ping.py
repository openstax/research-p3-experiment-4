from flask_restplus import Resource

from digital_logic.core import api

ns = api.namespace('ping', description='Check if the api is up')


@ns.route('/')
class Ping(Resource):
    def get(self):
        return {'message': 'pong'}
