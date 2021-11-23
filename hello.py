from flask import Flask, render_template, url_for, request

app = Flask(__name__)


menu = {'Home': 'index', "Brand": "brands"}

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", menu=menu, title="Homepage", pagename="homepage", footer="link")

@app.route("/brands", methods=["GET", "POST"])
def brands():
    if request.form.getlist("rate") == ["1-star"]:
        return render_template("index.html", menu=menu, title="Homepage", pagename="homepage", footer="link")
    elif request.form.getlist("rate") == ["3-star"]:
        return render_template("index.html", menu=menu, title="Homepage", pagename="3 start page", footer="link")
    return render_template("brands.html", menu=menu, title="Brands", pagename="coffee brands", footer="link")


if __name__ == "__main__":
    app.run(debug=True)