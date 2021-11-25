from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.secret_key = "&F)J@NcCfUjXn2r5u8x/y?D(G-KaPdSb"

menu = {'Home': 'index', "Brands": "brands", "Products": "products" }
brands_list = ["Julius Meinl", "Illy", "Movenpick", "Malongo"]
footer = "http://bengusta.com.ua"

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", menu=menu, title="Homepage", pagename="homepage", footer=footer)

@app.route("/brands")
def brands():
    return render_template("brands.html", menu=menu, title="Brands", pagename="All coffee brands", footer="link")

@app.route("/brand/<string:brand>")
def brand(brand):
    if brand.capitalize() in brands_list:
      return render_template("brand.html", menu=menu, body=brand.capitalize(), title=brand.capitalize(), footer="link")
    return render_template("404.html", menu=menu, body=brand, title="404 page not found", footer="link")

@app.route("/product")
def product():
    return render_template("product.html", menu=menu, title="Product", pagename="Product details", footer="link")


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "POST":
        if request.form.getlist("rate") == ["1-star"]:
            flash("You poor thing, get your 1 star products.")
            return render_template("products.html", menu=menu, title="All products", pagename="1 star products page", footer="link")
        elif request.form.getlist("rate") == ["3-star"]:
            flash("Here are your 3 star products, you little snob.")
            return render_template("products.html", menu=menu, title="All products", pagename="3 star products page", footer="link")
    return render_template("products.html", menu=menu, title="Products", pagename="prodcuts", footer="link")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", menu=menu, title="404 page not found", footer="link"), 404

if __name__ == "__main__":
    app.run(debug=True)