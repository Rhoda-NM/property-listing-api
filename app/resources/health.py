from flask_restx import Namespace, Resource

health_ns = Namespace('Health', description='Health check operations')

@health_ns.route('/health')
class Health(Resource):
    def get(self):
        """Simple Health check """
        return {'status': 'OK'}