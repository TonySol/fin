from flask import Blueprint

web = Blueprint("web", __name__)
api = Blueprint("api", __name__)

from . import web_routes, api_routes