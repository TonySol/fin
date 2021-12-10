"""This is a routing for api calls

Used Blueprint for routing, using URL prefix /or subdomain(preferebly).
Intended use to implement extended resources management logic (bulk).
Integrated JWT to handle naaccess.
"""

from flask import Blueprint

from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import sys
sys.path.append("..")

api = Blueprint("api", __name__)

from models.model import Department
from init import db

@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "admin":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@api.route("/getdata", methods=["GET"])
@jwt_required()
def getdata():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@api.route("/test")
def test():
    return "this is a test api route"
