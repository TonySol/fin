"""Describes REST API methods, parser, serialization to work with employee objects.

– `EmployeeItem` describes API methods for id related actions on employee entries
– `EmployeeList` describes API methods for bulk actions with employeee ntries

– resource_fields: describes field for marshalling
– parser: reqparse handle. Parses incoming JSON values.
"""
# pylint: disable=no-self-use, cyclic-import
from flask_restful import Resource, reqparse, fields, marshal_with, abort, inputs

from app.service.services import EmployeeService as emp_service
from app.rest import api


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'date_of_bidth': fields.DateTime(dt_format='iso8601'),
    'salary': fields.Integer,
    'dept_name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('surname', type=str)
parser.add_argument('salary', type=str)
parser.add_argument('date_of_bidth', type=inputs.date)
parser.add_argument('dept_name', type=str)


@api.resource('/employee/<int:id_no>')
class EmployeeItem(Resource):
    """A class holds id related API methods """

    @marshal_with(resource_fields)
    def get(self, id_no):
        """A handler for GET request.

        Fetches employee by id via service. Returns marshalled JSON with 200 status code.
        :param id: parsed from request URI
        :type id: int
        :raises error: 404 if wrong\non-existent id
        :return: JSON with department's entry data, 200 status code
        """
        result = emp_service.get_by_id(id_no)
        if not result:
            abort(404, message=f"Can't find entry with id {id_no}")
        return result

    def put(self, id_no):
        """A handler for PUT request.

        Deserializes JSON data from the request. Adds id to the deserialized dict.
        Validates it and provides to service. Returns 200 status code on success.

        :param id: parsed from request URI
        :type id: int
        :raises error: 404 if wrong\non-existent id, or validation failed.
        :return: 200 status code
        """
        args = parser.parse_args(strict=True)
        args["id"] = str(id_no)
        validated = emp_service.validate(args)

        if isinstance(validated, str):
            return f"Could not edit the entry: {validated}", 404

        result = emp_service.edit_entry(validated)
        if result:
            return f"The entry with id:{id_no} was changed successfully", 201
        return "Couldn't edit the entry: check if such employee exist.", 404

    def delete(self, id_no):
        """A handler for DELETE request.

        Deletes employee entry by id via services. Returns 204 status code on success.

        :param id: parsed from request URI
        :type id: int
        :raises error: 404 if wrong\non-existent id.
        :return: 204 status code
        """
        result = emp_service.delete_by_id(id_no)
        if result:
            return 204
        return f"The employee with id:{id_no} does not exists.", 404

@api.resource('/employee')
class EmployeeList(Resource):
    """A class holds bulk API methods for employees """

    @marshal_with(resource_fields)
    def get(self):
        """A handler for GET request.

        Fetches all employee entries via service. Returns marshalled JSON with 200 status code.
        :return: JSON with departments' entries data, 200 status code
        """
        result = emp_service.get_all()
        return result

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
            validated = emp_service.validate(args)
            if isinstance(validated, str):
                return f"Could not add the entry: {validated}", 404

            emp_service.add_entry(validated)
            return f"The entry with {args} was added successfully", 201
        return "The entry is missing required fields.", 404
