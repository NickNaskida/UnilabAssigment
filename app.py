# Unilab test assigment
#
# Project Author - Nikoloz Naskidashvili
# Project description - service booking system with ability to create and book services.
# Project reference - further project modifications may include users authentication system and documentation of api.

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializations
db = SQLAlchemy(app)  # Database
api = Api(app)  # API
marsh = Marshmallow(app)  # Marshmallow


# Database models
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    def __repr__(self):
        return f'<Service - {self.name}>'


# class Bookings(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     service =
#
#     def __repr__(self):
#         return f'<Service - {self.name}>'


# Schemas
class ServiceSchema(marsh.Schema):
    class Meta:
        fields = ("id", "name", "description")
        model = Service


service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


# Views
class Main(Resource):
    def get(self):
        return {
            'All services': {
                'docs': 'Get / Add services',
                'url': '/services',
                'methods': {
                    'GET': 'Returns all services from database',
                    'POST': 'Adds service to the database'
                }
            },
            'Get service': {
                'docs': 'Get service from database',
                'url': 'services/get/<service_id>',
                'arguments': '<service_id> - Integer'
            },
            'Edit service': {
                'docs': 'Edits service in database',
                'url': 'services/edit/<service_id>',
                'arguments': '<service_id> - Integer'
            },
            'Delete service': {
                'docs': 'Deletes service from database',
                'url': 'services/delete/<service_id>',
                'arguments': '<service_id> - Integer'
            }
        }


# Service
class Services(Resource):
    def get(self):
        services = Service.query.all()
        return services_schema.dump(services)

    def post(self):
        new_service = Service(
            name=request.json['name'],
            description=request.json['description']
        )
        db.session.add(new_service)
        db.session.commit()
        return service_schema.dump(new_service)


class GetService(Resource):
    def get(self, service_id):
        service = Service.query.get_or_404(service_id)
        return service_schema.dump(service)


class EditService(Resource):
    def put(self, service_id):
        service = Service.query.get_or_404(service_id)

        if 'name' in request.json:
            service.name = request.json['name']
        if 'description' in request.json:
            service.description = request.json['description']

        db.session.commit()
        return service_schema.dump(service)


class DeleteService(Resource):
    def delete(self, service_id):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return '', 204


# Booking
class GetServiceBookings(Resource):
    def get(self):
        return 'Get all service bookings'

    def post(self):
        return 'Book service'


class GetServiceBooking(Resource):
    def get(self, service_id):
        return 'Get service booking'


class EditServiceBooking(Resource):
    def put(self, service_id):
        return 'Edit service booking'


class DeleteServiceBooking(Resource):
    def delete(self, service_id):
        return 'Delete service booking'


api.add_resource(Main, '/')
api.add_resource(Services, '/services')
api.add_resource(GetService, '/services/get/<int:service_id>')
api.add_resource(EditService, '/services/edit/<int:service_id>')
api.add_resource(DeleteService, '/services/delete/<int:service_id>')
api.add_resource(GetServiceBookings, '/bookings')
api.add_resource(GetServiceBooking, '/bookings/get/<int:service_id>')
api.add_resource(EditServiceBooking, '/bookings/edit/<int:service_id>/')
api.add_resource(DeleteServiceBooking, '/bookings/delete/<int:service_id>')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
