from . import api

from flask_restful import Resource, reqparse, fields, marshal_with, abort
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
parser.add_argument('salary', type=str, location='json')
parser.add_argument('date_of_bidth', type=str, location='json')
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
        validated = emp_service.validate(args)
        if not isinstance(validated, dict):
            return f"Could not edit the entry: {validated}", 404

        result = emp_service.edit_entry(entry=validated, entry_id=id)
        if result:
            return f"The entry with id:{id} was changed successfully", 201
        return f"The employee with id:{id} does not exists.", 404

    def delete(self, id):
        result = emp_service.delete_by_id(id)
        if result:
            return "The entry has been deleted successfully", 204
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
            validated = emp_service.validate(args)
            if not isinstance(validated, dict):
                return f"Could not add the entry: {validated}", 404

            emp_service.add_entry(entry=validated)
            return f"The entry with {args} was added successfully", 201
        return f"The entry is missing required fields.", 404



