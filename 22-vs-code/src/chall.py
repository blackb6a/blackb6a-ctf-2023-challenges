
import json, re, subprocess, string
from os import path
from secret import flag
from Crypto.Cipher import AES

def find_user_extensions() -> list[str]:
    result = subprocess.run([
        "find",
        path.expanduser("~/.vscode-oss/extensions"),
        "-name",
        "package.json"
    ], stdout=subprocess.PIPE)
    return result.stdout.strip().decode().split("\n")

def open_and_parse_json(path):
    with open(path) as p:
        return json.load(p)

for package in find_user_extensions():
    data = open_and_parse_json(package)
    try:
        if "raccoon" in [x["id"] for x in data["contributes"]["languages"]]:
            for g in data["contributes"]["grammars"]:
                if g["scopeName"] == "source.raccoon":
                    rn_grammar = open_and_parse_json(
                        path.normpath(path.join(package, "..", g["path"]))
                    )
                    break
    except:
        continue

ws = open_and_parse_json(".vscode/settings.json")

def get_child(obj, paths):
    try:
        for p in paths:
            obj = obj[p]
        return obj
    except:
        return None

tmdrules = get_child(ws, ["editor.tokenColorCustomizations", "textMateRules"])

assert "keyword.control" == tmdrules[0]["scope"]
assert "constant.character.escape" in tmdrules[4]["scope"]

colors_1st_part = list(map(lambda x: x.replace("#",""), [
    get_child(ws,["workbench.colorCustomizations","minimap.selectionHighlight"]),
    get_child(ws,["editor.tokenColorCustomizations", "functions"]),
    tmdrules[0]["settings"]["foreground"],
    tmdrules[4]["settings"]["foreground"],
]))

assert all(len(x)==6 for x in colors_1st_part)

bt = get_child(rn_grammar, ["repository","builtin-types"])
assert bt["name"] == "support.type.raccoon"
colors_2nd_part = "".join(x for x in re.compile(bt["match"]).findall(bt["match"]) if 'U' in x)
assert len(colors_2nd_part) == 12

cipher = AES.new(bytes.fromhex("".join(colors_1st_part))+colors_2nd_part.encode(), AES.MODE_CTR, nonce=b"")

assert flag == "b6actf{0n3_sM4LL_maP_f0R_Man;1_GiAn7_Fl4g_4_y4'all}" # no escape
inside = re.compile(r"""
^
\x62    # different escapes
\u0036  # TIL I can put comments in regex
\141    # How cool
ctf\{([!-z]{43})\}
""", re.X).match(flag)[0].encode()

assert cipher.encrypt(inside).hex() == "503dffdf68de1a94143572e1303fd357559f11d876d507ca674a4bf621d6c1e44c8a0f3e9cfc93dbedfb54f00aa8bcde796d15"

if __name__ == "__main__":
    filename = path.basename(__file__)

    with open(f'./{filename}') as f:
        data = f.read()

    with open('./ciphertext') as f:
        translation = str.maketrans(string.digits+string.ascii_letters, f.read().rstrip())

    with open(F'./{filename.translate(translation)}', 'w') as f:
        f.write(data.translate(translation))
