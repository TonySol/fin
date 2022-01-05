"""This is a routing for api calls

Used Blueprint for routing, using URL prefix /or subdomain(preferebly).
Intended use to implement extended resources management logic (bulk).
Integrated JWT to handle naaccess.
"""

from . import api
from . import api_bp

from flask_restful import Resource, reqparse, inputs, fields, marshal_with
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

class DepartmenteItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)


    @marshal_with(resource_fields)
    def get(self, name):
        result = dept_service.get_by_prime_key(name)
        return result

    def put(self, name):
        args = self.parser.parse_args(strict=True)
        task = {}
        return task, 201

class DepartmentList(Resource):
    pass

api.add_resource(DepartmenteItem, '/department/<string:name>')
api.add_resource(DepartmentList, '/department')