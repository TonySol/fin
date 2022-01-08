from app.views import web
from app import db

from flask import render_template


@web.route("/")
@web.route("/index")
def index():
    return render_template("index.html",
                           title="Examine your departments",
                           pagename="Homepage")

@web.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404 page not found"), \
           404

@web.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title="500 error has occurred"), 500