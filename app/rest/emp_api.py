from . import api

from flask_restful import Resource, reqparse, inputs, fields, marshal_with, abort
from app.service.services import EmployeeService as emp_service

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'date_of_bidth': fields.DateTime(dt_format='iso8601'),
    'salary': fields.Integer,
    'dept_name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json')
parser.add_argument('surname', type=str, location='json')
parser.add_argument('salary', type=int, location='json')
parser.add_argument('date_of_bidth', type=inputs.date, location='json')
parser.add_argument('dept_name', type=str, location='json')


@api.resource('/employee/<int:id>')
class EmployeeItem(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        result = emp_service.get_by_id(id)
        if not result:
            abort(404, message=f"Can't find entry with id {id}")
        return result

    def put(self, id):
        args = parser.parse_args(strict=True)
        result = emp_service.edit_entry(args, entry_id=id)
        if result:
            return f"The entry with id:{id} was changed successfully", 201
        return f"The employee with id:{id} does not exists.", 404

    def delete(self, id):
        result = emp_service.delete_by_id(id)
        if result:
            return "The entry has been deleted seccessfully", 204
        return f"The employee with id:{id} does not exists.", 404

@api.resource('/employee')
class EmployeeList(Resource):

    @marshal_with(resource_fields)
    def get(self):
        result = emp_service.get_all()
        return result

    def post(self):
        args = parser.parse_args(strict=True)
        if all(i for i in args.values()):
            emp_service.add_entry(args)
            return f"The entry with {args} was added successfully", 201
        return f"The entry is missing required fields.", 404



