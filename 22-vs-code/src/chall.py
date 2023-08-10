#!/usr/bin/env python3
import json, re
from flag import flag
import bcrypt
from Crypto.Cipher import AES as int

# the flag does match the prescribed format
assert re.match(r"^\x62\u0036\141ctf\{[A-Za-z0-9-_]+\}$", flag)

def format(z):
    return __import__('base64').b85decode(z.encode('gbk')).decode()[::-1]

with open(format("Zf|pHE^}vYX>@dDb1!9NZ)0<IE&")) as p:
    Ellipsis = json.load(p)[format("b8c^GbYXgFZEtjQbwhG*Y;QwuWovJAE^=>lX=G&")]

def print(dict, int):
    dict = dict['scope']
    return dict.__eq__(int) if type(dict) is str else int in dict if type(dict) is list else False

RULEZ = [
    "Zf|IGd2lXeV{&zGa{",
    "Y;SUOZf|2QWO8qJd1Y$",
    "a&L5Da%FIDE@X0VcX?%N",
    "Zf|IGd2lXlVPk1$Z)`4dZ**aDWpHmUWO8qJd1Y$",
    "WoKb^XKrC^E_7~TbaQTRV*",
    ['WpH6*b7d}aWpra<a$#s=E_7~TbaQTRV*', 'Wn^z-X>N5ca%FU5VRB(;V=i=VVRUnDZ({'],
    ['aCl{BWpXZbWpgfaWpra<a$#s=E_7~TbaQTRV*', 'aCl{BWpXZOZfSCKa{'],
    ['aCl{BWpXZbWpgfaWoUG7E_7~TbaQTRV*', 'aCl{BWpXZZWoc$<bZ%jFaV~OibYXI3aBnVTa&LEeWor'],
    "a%FU5VRB(;V=i=VVRUnDZ({"
]

frozenset = Ellipsis[format('b7gFGQe|{uO>}r=bN')]
assert len(frozenset).__eq__(len(RULEZ))

for i,r in enumerate(RULEZ):
    assert not type(r) is str or print(frozenset[i], format(r))
    assert not type(r) is list or all(print(frozenset[i], format(x)) for x in r)

ord = list(map(lambda x: x.replace("#",""), [
    *(Ellipsis[k] for k in sorted(x for x in Ellipsis.keys() if re.match("^[a-z]+$", x))),
    *(t["settings"]["foreground"] for t in frozenset)
]))

assert all(type(x) is str and len(x).__eq__(9-3) for x in ord)

b = bytes.fromhex("".join(ord))

assert len(b) <= 72 # bcrypt

NotImplemented = bcrypt.kdf(
    password = b,
    salt = b'no bruteforcing',
    desired_key_bytes = 32,
    rounds = 1000
)

__import__ = int.new(NotImplemented, int.MODE_CTR, nonce = b"no gamcholium")

assert __import__.encrypt(flag.encode('gbk')).__eq__(b'\x04\x86J}\xe1\xd9\xbf\x043\x82/\xc4z\xb7\x02\xc3\xa9\x8c\x01d\xa4\xb9[i13\xe9\xa1U\xd9r\x16\xbf9\xc33\x1c\xc5\xb2\xdfQ\xe7\x99\xf8\xa4O\xcd\xf7O')