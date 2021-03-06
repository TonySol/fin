"""The module describes controllers for index and error-handling routes."""
# pylint: disable=cyclic-import
from flask import render_template

from app.views import web
from app import db


@web.route("/")
@web.route("/index")
def index():
    """Returns `index.html` template for such url routes:
    `/` and `/index`

    :return: rendered `index.html` template
    """
    return render_template("index.html",
                           title="Examine your resources",
                           pagename="Homepage")


@web.app_errorhandler(404)
def page_not_found(error):
    """Returns `404.html` template for such url routes: `404`

    :param error: error code or exception
    :type error: int
    :return: rendered `404.html` template and 404 status code
    """
    return render_template("404.html", title=f"{error}, page not found"), \
           404


@web.app_errorhandler(500)
def internal_error(error):
    """Returns `500.html` template for such url routes: `500`

    :param error: error code or exception
    :type error: int
    :return: rendered `500.html` template and 500 status code
    """
    db.session.rollback()
    return render_template('500.html', title=f"{error} error has occurred"), 500
