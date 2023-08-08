# Skills required: Data analysis

In this challenge, players receive a png file taken from the *minimap* of VSCode[1] as hinted at title. By default `editor.minimap.renderCharacters` is on and this can leak the whole program, given sufficient code text.

While the source code syntax coloring is customized (we'll go through that later), it is highly reminiscent of Python. To increase the fun and reduce bruteforcing though, I have:

- Increased bcrypt rounds to 13
- Append actual colors used before hashing
- changed the background to #202020 to be more theme agnostic

Here's a suggested solve path:

1. Solve the cryptogram
1. Identify exactly the various text colors
1. Understanding the workspace setting
1. Get flag

### Solve the cryptogram

There are many ways to approach this part since the characters themselves are intact.

It is possible to recover 99% of the program, aside from some hard to distinguish characters like `/` vs `\`, `s` vs `{` vs `}`. It is however possible to sort them out by context.

```py
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
```

### Identify exactly the various text colors

Knowing the program plaintext allows us to reverse the colors blazing fast. This challenge works in the first place because minimap (at zoom level 1) is font agnostic as demonstrated [in the actual official source code](https://github.com/microsoft/vscode/blob/main/src/vs/editor/browser/viewParts/minimap/minimapPreBaked.ts)

There are minute details like whether to `round` or `floor`. If replicating it seems to much, it's advisable to create your own image where everything's well-known.

Usually it takes 2~6 characters to completely determine the color.

```py
from itertools import chain
from math import floor
from sage.all import vector, RR
from PIL import Image

intensities = '0000511D6300CF609C709645A78432005642574171487021003C451900274D35D762755E8B629C5BA856AF57BA649530C167D1512A272A3F6038604460398526BCA2A968DB6F8957C768BE5FBE2FB467CF5D8D5B795DC7625B5DFF50DE64C466DB2FC47CD860A65E9A2EB96CB54CE06DA763AB2EA26860524D3763536601005116008177A8705E53AB738E6A982F88BAA35B5F5B626D9C636B449B737E5B7B678598869A662F6B5B8542706C704C80736A607578685B70594A49715A4522'

pixels = [floor(int(intensities[i:i+2], base=16)*4/5) for i in range(0,len(intensities),2)]

pairs = [vector(pixels[i:i+2]) for i in range(0,len(pixels),2)]

def gen_reference(s, coord):
    return [((coord[1]-1+i, coord[0]-1),c) for i,c in enumerate(s)]

with Image.open("../public/chall.png") as im:
    rgb_im = im.convert('RGB')
    bg = vector(rgb_im.getpixel((rgb_im.width-1,0)))

    def calculate(*references):
        reference = list(chain(*chain(gen_reference(*r) for r in references)))

        candidates = [list(range(256)) for _ in range(3)]
        for coord, letter in reference:
            pair_info = [
                tuple(vector(rgb_im.getpixel((coord[0],coord[1]*2+i)))-bg) for i in range(2)
            ]
            channels = tuple(zip(*pair_info))
            for i, ch in enumerate(channels):
                temp = [x for x in candidates[i] if tuple(round(x) for x in pairs[ord(letter)-32]*(x-bg[0])/255) == ch]
                # if len(temp) != len(candidates[i]):
                #     print(letter, pairs[ord(letter)-32])
                candidates[i] = temp
                if len(candidates[i]) == 0:
                    print(f"Channel #{i} failed")
            
            if all(len(x)==1 for x in candidates):
                print(letter, *[hex(l[0])[2:] for l in candidates])
                break
        else:
            print(letter, *[[hex(x)[2:] for x in l] for l in candidates])
    
    calculate(("#!/usr/bin/env python3", (1,1)))
    calculate(("import", (2,1)))
    calculate(("json, re", (2,8)))
    calculate(("\\x62\\u0036\\141", (8,20)))
    calculate(("A-Za-z0-9-_", (8,40)))
    calculate(
        ("[", (8,39)),
        ("]+", (8,51)),
    )
    calculate(
        ('def', (10,1))
    )
    calculate(
        ('.vscode/settings.json', (14,12))
    )
    calculate(
        ('type', (18,24))
    )
    calculate(
        ('in', (18,48)),
        ('or', (37,26)),
    )
    calculate(
        ('False', (18,77))
    )
    calculate(
        ('enumerate', (34,12))
    )
    calculate(
        ('*', (43,5)),
        ('<=', (51,15)),
    )
    calculate(
        ('72', (51,18)),
        ('32', (56,25)),
    )
    calculate(
        ('password', (54,5)),
    )
```

### Understanding the workspace setting

Theme colorization is governed by the workspace setting at `.vscode/settings.json`, under `editor.tokenColorCustomizations`

Besides the known entries under `textMateRules`, there are also:

```
comments
functions
keywords
numbers
strings
types
variables
```

The `Ctrl+Shift+P` `Developer: Inspect Editor Tokens and Scopes` hotkey could be handy:

|categories|color|keywords or remark|
|-|-|-|
|comments| #315528 | comments |
|functions| #6cf73e | builtin functions like `open`,`len`,`map` excluding types<br/>function names in declarations |
|keywords| #279c00 | `def` and `lambda` (and also `r` in regex string) |
|numbers| #f5e6a0 | plain numbers |
|strings| #138f13 | plain string,<br/>regex strings are rendered a bit differently |
|types| #49d11b | `int`, `tuple`, `Exception` |
|variables| #ccdd99 | function parameters and named arguments |
|source.python|#5a8f5a| variables and modules, overrides function calls |
|keyword.control|#beff33| `import`, `from`, `if`... |
|keyword.operator|#ffffbe| `<`, `=`, `*`, `+` |
|keyword.operator.logical.python|#00ff00| only `or` and `in` are shown.<br/>Doesn't apply to `for _ in _` |
|constant.language|#ecff58| only `False` |
|constant.character.escape,<br/>constant.character.unicode|#85c656| used to deter guessing |
|constant.character.set.regexp,<br/>string.regexp|#defaca| plain string and character sets in regexs |
|constant.other.set.regexp<br/>keyword.operator.quantifier.regexp|#acfe09| Touches up so that `[]+` doesn't look out of place.<br/>**The only undetermined color `#acfe0[89a]`** |

### Get your flag and profit!

Notes:
- [1] Actually Codium is used.