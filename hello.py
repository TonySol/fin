from flask import Flask, render_template


app = Flask(__name__)



menu = {'Home': '/index', "Brand": "/brands"}

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", menu=menu, title="Homepage", pagename="homepage", footer="link")

@app.route("/brands")
def brands():
    return render_template("brands.html", menu=menu, title="Brands", pagename="coffee brands", footer="link")


if __name__ == "__main__":
    app.run(debug=True)