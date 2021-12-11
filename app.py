from flask import Flask

app = Flask(__name__)

@app.route("/<id>")
def index(id):
    return render_template("index.html", id=id)
