from flask import Flask, render_template, session
from flask_session import Session
from werkzeug.exceptions import HTTPException
import json
import os
from uuid import uuid4

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid4()
Session(app)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return render_template("template.html", status="500", message=e), 500
    return render_template("template.html", status="500", message=str(e)), 500

@app.route("/<path:path>")
def render(path):
    if not os.path.exists(f"templates/{path}"):
        return render_template("template.html", status="404", message="not found"), 404
    return render_template(f"{path}")

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/flag")
def flag():
    if session["user"] is not "admin":
        return render_template("template.html", status="403", message="You are not admin."), 403
    return render_template("template.html", status="200", message=os.environ("FLAG")), 200  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000")