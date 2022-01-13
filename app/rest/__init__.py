"""The package contains REST API modules:

– `dept_api`: holds classes that describe api methods for department entries
– `emp_api`: holds classes that describe api methods for employees entries

Here we create Blueprint instance for api routes.
In turn, we pass flask blueprint object to the flask restful in order to initialise it.

Import modules afterwards thus avoiding circular import.
"""


from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api_bp", __name__)
api = Api(api_bp)

from . import dept_api, emp_api