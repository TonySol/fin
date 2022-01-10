"""This is a routing for api calls

Used Blueprint for routing, using URL prefix /or subdomain(preferebly).
Intended use to implement extended resources management logic (bulk).
Integrated JWT to handle naaccess.
"""

from . import api

from flask_restful import Resource, reqparse, fields, marshal_with, abort
from app.service.services import DepartmentService as dept_service


resource_fields = {
    'id': fields.Integer,
    'name': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


@api.resource('/department/<int:id>')
class DepartmentItem(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        result = dept_service.get_by_id(id)
        if not result:
            abort(404, message=f"Can't find entry with id {id}")
        return result, 200

    def put(self, id):
        args = parser.parse_args(strict=True)
        args["id"] = str(id)
        validated = dept_service.validate(args)
        if isinstance(validated, str):
            return f"Could not edit the entry: {validated}", 404

        result = dept_service.edit_entry(validated)
        if result:
            return f"The entry with id:{id} was changed successfully", 201
        return f"The entry with id:{id} does not exists.", 404

    def delete(self, id):
        result = dept_service.delete_by_id(id)
        if result > 0:
            return 204
        return f"The entry with id:{id} does not exists.", 404

@api.resource('/department')
class DepartmenteList(Resource):

    @marshal_with(resource_fields)
    def get(self):
        result = dept_service.get_all()
        return result

    def post(self):
        args = parser.parse_args(strict=True)
        if all(i for i in args.values()):
            validated = dept_service.validate(args)
            if isinstance(validated, str):
                return f"Could not add the entry: {validated}", 404

            dept_service.add_entry(validated)
            return f"The entry with {args} was added successfully", 201
        return f"The entry is missing some fields.", 404
