"""The package holds modules with such controllers:

– `basic` module contains controllers for error pages and homepages
– `dept_routes` module contains departmen-related controllers
– `emp_routes` module contains employee-related controllers

:param web: is a Blueprint instance for web controllers

Import modules afterwards thus avoiding circular import.
"""

from flask import Blueprint

web = Blueprint("web", __name__)

from . import basic, emp_routes, dept_routes