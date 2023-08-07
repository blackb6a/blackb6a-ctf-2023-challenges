#!/usr/bin/env python3
import json, re, subprocess
from flag import flag
import bcrypt

# the flag does match the prescribed format
assert re.match(r"^\x62\u0036\141ctf\{[A-Za-z0-9-_]+\}$", flag)

def oapj(path):
    with open(path) as p:
        return json.loads(re.sub("//.*","",p.read(),flags=re.M))

ws = oapj(".vscode/settings.json")["editor.tokenColorCustomizations"]

def inscope(rule, val):
    r = rule['scope']
    return r==val if type(r)==str else val in r if type(r)==list else False

rules=[
    "source.python",
    "keyword.control",
    "keyword.operator",
    "keyword.operator.logical.python",
    "constant.language",
    ["constant.character.escape","constant.character.unicode"],
    ["constant.character.set.regexp","string.regexp"],
]

tmdrules = ws['textMateRules']
assert len(tmdrules) == len(rules)
for i,r in enumerate(rules):
    if type(r)==str:
        assert inscope(tmdrules[i], r)
    elif type(r)==list or type(r)==tuple:
        assert all(inscope(tmdrules[i], x) for x in r)
    else:
        raise Exception("0 mark redo")

colors = list(map(lambda x: x.replace("#",""), [
    *(ws[k] for k in sorted(x for x in ws.keys() if re.match("^[a-z]+$", x))),
    *(t["settings"]["foreground"] for t in tmdrules)
]))

assert all(type(x) == str and len(x)==6 for x in colors)

peppered_flag = flag.encode('utf-8') + bytes.fromhex("".join(colors))

assert len(peppered_flag)<=72 # bcrypt

# every trial counts
assert bcrypt.checkpw(peppered_flag, b'$2b$13$6Od/kTTrv619HcJUWmu9yO1UNiz.sdzpeIz.HwaAxVUR46l05Lxsm')