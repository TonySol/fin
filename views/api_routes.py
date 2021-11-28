from flask import Blueprint, render_template, url_for, request, flash, redirect
api = Blueprint("api_v1", __name__)

@api_v1.route("/api")
def api():
    return render_template("index.html", title="Coffee matching page", pagename="coffee matching machine!",
                           footer="link")

