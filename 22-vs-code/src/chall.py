#!/usr/bin/env python3
import json, re
from flag import flag
import bcrypt
from Crypto.Cipher import AES

# the flag does match the prescribed format
assert re.match(r"^\x62\u0036\141ctf\{[A-Za-z0-9-_]+\}$", flag)

def oapj(path):
    with open(path) as p:
        return json.load(p)

ws = oapj(".vscode/settings.json")["editor.tokenColorCustomizations"]

def inscope(rule, val):
    r = rule['scope']
    return r == val if type(r) == str else val in r if type(r) == list else False

rules = [
    "source.python",
    "keyword.control",
    "keyword.operator",
    "keyword.operator.logical.python",
    "constant.language",
    ["constant.character.escape", "constant.character.unicode"],
    ["constant.character.set.regexp", "string.regexp"],
    ["constant.other.set.regexp", "keyword.operator.quantifier.regexp"]
]

tmdrules = ws['textMateRules']
assert len(tmdrules) == len(rules)

for i,r in enumerate(rules):
    if type(r) == str:
        assert inscope(tmdrules[i], r)
    elif type(r) == list or type(r) == tuple:
        assert all(inscope(tmdrules[i], x) for x in r)
    else:
        raise Exception("0 mark redo")

colors = list(map(lambda x: x.replace("#",""), [
    *(ws[k] for k in sorted(x for x in ws.keys() if re.match("^[a-z]+$", x))),
    *(t["settings"]["foreground"] for t in tmdrules)
]))

assert all(type(x) == str and len(x) == 6 for x in colors)

b = bytes.fromhex("".join(colors))

assert len(b) <= 72 # bcrypt

secure_key = bcrypt.kdf(
    password = b,
    salt = b'no bruteforcing',
    desired_key_bytes = 32,
    rounds = 1000
)

cipher = AES.new(secure_key, AES.MODE_CTR, nonce = b"no gamcholium")

assert cipher.encrypt(flag.encode('utf-8')).hex() == "d00fbaacc1691ff2d068aa659c438fbd6e046bd1ce1b5eb472927bf0934f19eccb688400c26415a5ccf23e7564c6812a73"