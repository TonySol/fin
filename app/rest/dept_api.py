"""This is a routing for api calls

Used Blueprint for routing, using URL prefix /or subdomain(preferebly).
Intended use to implement extended resources management logic (bulk).
Integrated JWT to handle naaccess.
"""

from . import api
from . import api_bp

from flask_restful import Resource, reqparse, fields, marshal_with, abort
from app.service.services import DepartmentService as dept_service

from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


@api_bp.route("/login", methods=["POST"])
def login():
    """Login route – a gateway api access"""
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "admin":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@api_bp.route("/getdata", methods=["GET"])
@jwt_required()
def getdata():
    """Simple get data request route

    Works via jwt identifier.
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


resource_fields = {
    'name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


@api.resource('/department/<string:name>')
class DepartmentItem(Resource):

    @marshal_with(resource_fields)
    def get(self, name):
        result = dept_service.get_by_id(name)
        if not result:
            abort(404, message=f"Can't find entry with id {name}")
        return result

    def put(self, name):
        args = parser.parse_args(strict=True)
        validated = dept_service.validate(args)
        if not isinstance(validated, dict):
            return f"Could not edit the entry: {validated}", 404

        result = dept_service.edit_entry(entry=validated, entry_id=name)
        if result:
            return f"The entry with id:{name} was changed successfully", 201
        return f"The entry with id:{name} does not exists.", 404

    def delete(self, name):
        result = dept_service.delete_by_id(name)
        if result > 0:
            return 204
        return f"The entry with id:{name} does not exists.", 404

@api.resource('/department')
class DepartmenteList(Resource):
    parser_copy = parser.copy()
    parser_copy.replace_argument('name', action="append")

    @marshal_with(resource_fields)
    def get(self):
        result = dept_service.get_all()
        return result

    def post(self):
        args = parser.parse_args(strict=True)
        if all(i for i in args.values()):
            validated = dept_service.validate(args)
            if not isinstance(validated, dict):
                return f"Could not add the entry: {validated}", 404

            dept_service.add_entry(entry=validated)
            return f"The entry with {args} was added successfully", 201
        return f"The entry is missing some fields.", 404

    def delete(self):
        args = self.parser_copy.parse_args(strict=True)
        deleted_names = []
        for name in args["name"]:
            result = dept_service.delete_by_id(name)
            if result:
                deleted_names.append(name)
        return f"The following entries have been deleted successfully: {deleted_names}", 200