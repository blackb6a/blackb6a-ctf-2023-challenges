from flask import Flask, render_template, session, request, Response
from flask_session import Session
from werkzeug.exceptions import HTTPException
import os
from uuid import uuid4
from utils import Blog

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid4()
Session(app)

blogs = Blog()

# @app.errorhandler(Exception)
# def handle_exception(e):
#     if isinstance(e, HTTPException):
#         return e
#     return str(e), 500

# @app.after_request
# def after_request_callback(response: Response):
#     # print(response.__dict__)
#     if response.status_code >= 500:
#         updated = render_template("template.html", status=response.status_code, message=response.response[0].decode())
#         response.set_data(updated)
#     return response

@app.route("/<path:path>")
def render(path):
    if not os.path.exists(f"templates/{path}"):
        return render_template("template.html", status=404, message="not found")
    return render_template(f"{path}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/load_blogs", methods=["POST"])
def load_blogs():
    if request.headers.get("Content-Type") != "application/json":
        raise Exception("A JSON-like object is required.")
    blogs.load(request.data)
    return {"message": "Blog loaded."}

@app.route("/get_blogs", methods=["POST"])
def get_blogs():
    try:
        return blogs.read()
    except:
        return blogs.__dict__
        
@app.route("/flag")
def flag():
    if session.get("user") != "admin":
        return render_template("template.html", status=403, message="You are not admin.")
    return render_template("template.html", status=200, message=os.environ("FLAG"))

@app.route("/test")
def test():
    return f"[+]{blogs.__dict__}\n[+]Config:%s"%(app.config['SECRET_KEY'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000")