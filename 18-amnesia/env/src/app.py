from flask import Flask, render_template, Response, request
import secrets
from werkzeug.exceptions import HTTPException
import json
import os
import jwt


app = Flask(__name__)
app.secret_key = secrets.token_bytes()

f = open("jwks.json")
jwks_content = f.read()
f.close()

FLAG = os.getenv("FLAG")

valid_algo = "RS256"

def is_valid_algo(token):
    headers = jwt.get_unverified_header(token)
    algo = headers["alg"]
    return algo == valid_algo

def authorize_token(token):
    if not is_valid_algo(token):
        raise Exception(f"Only {valid_algo} is allowed.")
    public_key = json.loads(jwks_content)["keys"][0]["x5c"][0]
    public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    decoded_token = jwt.decode(token, public_key, algorithms=[valid_algo])
    if "user" not in decoded_token:
        raise Exception("\"user\" claim required")
    if decoded_token["user"] == "memory hero":
        return True
    return False

@app.after_request
def after_request_callback(response: Response):
    print(response.__dict__)
    if response.headers["Content-Type"].startswith("text/html"):
        updated = render_template("index.html", status=response.status_code, message=response.response[0].decode())
        response.set_data(updated)
    if "auth" not in request.cookies:
        response.set_cookie("auth", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoibWVtb3J5IGxvc3QifQ.Fw-zd72pKScg-Zagzz_zl04doz84NgG2uPjr3yAcYu3DJ0Kp5rLaprBRKyQwdJ1232A791WQSaByIAwawzQsZ4XO8aVg6xmnnXEpHXU0Yb88jmNdP6jcjnOxyQ9zTpyQsnoy_raqYWhELCizXn-Y9QwKDXYk2WT1UMdWtLuZ4DYC043Y5glKlaVFTLhpilIPh5h3NlCRxdR9KSnPUO0ZK-8Bahw3onBTsjBgcK7exJLp374dGrdeijaM1jcCRzhb4SGpHHvT_JGYvTfQJW4P7JQM3u8dC4eK06bYwl3QGIlWqxGxc53IBGMzfkDUcEYYg5HCplDnJe-o128RxokUBQ")
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return str(e), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return "Flag at /flag", 200

@app.route("/.well-known/jwks.json")
def jwks():
    return jwks_content, 200, {"Content-Type": "application/json"}

@app.route("/flag")
def flag():
    if "auth" not in request.cookies:
        raise Exception("Authorization cookie required.")
    if not authorize_token(request.cookies.get("auth")):
        return "Not authorized. Only \"memory hero\" can get the flag.", 403
    else:
        return f"Welcome! The flag is {FLAG}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000")