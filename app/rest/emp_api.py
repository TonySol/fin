from . import api

from flask_restful import Resource, reqparse, inputs, fields, marshal_with
from app.service.services import EmployeeService as emp_service

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'date_of_bidth': fields.DateTime(dt_format='iso8601'),
    'salary': fields.Integer,
    'dept_name': fields.String,
}


class EmployeeItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('name', type=str)
    parser.add_argument('surname', type=str)
    parser.add_argument('salary', type=int)
    parser.add_argument('date_of_bidth', type=inputs.date)
    parser.add_argument('dept_name', type=str)

    @marshal_with(resource_fields)
    def get(self, id):
        result = emp_service.get_by_prime_key(id)
        return result

    def put(self, id):
        args = self.parser.parse_args(strict=True)
        task = {}
        return task, 201

class EmployeeList(Resource):
    pass

api.add_resource(EmployeeItem, '/employee/<int:id>')
api.add_resource(EmployeeList, '/employee')