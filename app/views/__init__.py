from flask import Blueprint

web = Blueprint("web", __name__)

from . import basic, emp_routes, dept_routes