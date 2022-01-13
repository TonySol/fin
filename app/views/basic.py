from app.views import web
from app import db

from flask import render_template


@web.route("/")
@web.route("/index")
def index():
    """Returns `index.html` template for such url routes:
    `/` and `/index`

    :return: rendered `index.html` template
    """
    return render_template("index.html",
                           title="Examine your departments",
                           pagename="Homepage")

@web.app_errorhandler(404)
def page_not_found(error):
    """Returns `404.html` template for such url routes: `404`

    :param error: error code or exception
    :type error: int
    :return: rendered `404.html` template and 404 status code
    """
    return render_template("404.html", title="404 page not found"), \
           404

@web.app_errorhandler(500)
def internal_error(error):
    """Returns `500.html` template for such url routes: `500`

    :param error: error code or exception
    :type error: int
    :return: rendered `500.html` template and 500 status code
    """
    db.session.rollback()
    return render_template('500.html', title="500 error has occurred"), 500