"""Describes REST API methods, parser, serialization to work with department objects.

– `DepartmentItem` describes API methods for id related actions
– `DepartmentsList` describes API methods for bulk actions

– resource_fields: describes field for marshalling
– parser: reqparse handle. Parses incoming JSON values.
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
    """A class holds id related API methods """

    @marshal_with(resource_fields)
    def get(self, id):
        """A handler for GET request.

        Fetches department by id via service. Returns marshalled JSON with 200 status code.
        :param id: parsed from request URI
        :type id: int
        :raises error: 404 if wrong\non-existent id
        :return: JSON with department's entry data, 200 status code
        """
        result = dept_service.get_by_id(id)
        if not result:
            abort(404, message=f"Can't find entry with id {id}")
        return result, 200

    def put(self, id):
        """A handler for PUT request.

        Deserializes JSON data from the request. Adds id to the deserialized dict.
        Validates it and provides to service. Returns 200 status code on success.

        :param id: parsed from request URI
        :type id: int
        :raises error: 404 if wrong\non-existent id, or validation failed.
        :return: 200 status code
        """
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
        """A handler for DELETE request.

        Deletes department entry by id via services. Returns 204 status code on success.

        :param id: parsed from request URI
        :type id: int
        :raises error: 404 if wrong\non-existent id.
        :return: 204 status code
        """
        result = dept_service.delete_by_id(id)
        if result > 0:
            return 204
        return f"The entry with id:{id} does not exists.", 404

@api.resource('/department')
class DepartmentsList(Resource):
    """A class holds bulk API methods for departments """

    @marshal_with(resource_fields)
    def get(self):
        """A handler for GET request.

        Fetches all departments via service. Returns marshalled JSON with 200 status code.
        :return: JSON with departments' entries data, 200 status code
        """
        result = dept_service.get_all()
        return result, 200

    def post(self):
        """A handler for POST request.

        Deserializes JSON data from the request. Checks if all resource_fields supplied
        Validates deserialized dict of params and provides to the service.
        Returns 200 status code on success.

        :raises error: 404 if wrong\non-existent id, or validation failed.
        :return: 200 status code
        """
        args = parser.parse_args(strict=True)
        if all(i for i in args.values()):
            validated = dept_service.validate(args)
            if isinstance(validated, str):
                return f"Could not add the entry: {validated}", 404

            dept_service.add_entry(validated)
            return f"The entry with {args} was added successfully", 201
        return f"The entry is missing some fields.", 404
