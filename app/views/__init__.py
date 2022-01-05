from flask import Blueprint

web = Blueprint("web", __name__)

from . import web_routes