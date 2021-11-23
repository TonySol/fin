from flask import Flask, render_template, url_for, request

app = Flask(__name__)


menu = {'Home': 'index', "Brand": "brands", "Product": "product" }

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", menu=menu, title="Homepage", pagename="homepage", footer="link")

@app.route("/brands")
def brands():
    return render_template("brands.html", menu=menu, title="Brands", pagename="coffee brands", footer="link")

@app.route("/product", methods=["GET", "POST"])
def product():
    if request.form.getlist("rate") == ["1-star"]:
        return render_template("index.html", menu=menu, title="Homepage", pagename="1 star product page", footer="link")
    elif request.form.getlist("rate") == ["3-star"]:
        return render_template("index.html", menu=menu, title="Homepage", pagename="3 star products page", footer="link")
    return render_template("product.html", menu=menu, title="Brands", pagename="prodcuts", footer="link")

if __name__ == "__main__":
    app.run(debug=True)