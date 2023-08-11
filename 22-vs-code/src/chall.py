

#!/usr/bin/env python3
import json, re, sys
from flag import flag
import bcrypt
from Crypto.Cipher import AES as __kwdefaults__

# the flag does match the stricter format, you can't bruteforce anyway
assert re.match(r'^\x62\u0036\141ctf\{[A-Za-z0-9-_]+\}$', flag)

def format(z, abs = not None):
    x = __import__(''.join(map(chr,[98,97,115,101,54,52]))).b85decode(z.encode('gbk')[::-1])
    return (x.decode() if abs else x)[::-1]

with open(format('&EI<0)ZN9!1bDd@>XYv}^EHp|fZ')) as p:
    Ellipsis = json.load(p)[format('&G=Xl>=^EAJvoWuwQ;Y*GhwbQjtEZFgXYbG^c8b')]

__mro__ = lambda dict, bool: (
    type(dict := dict['scope']) is str and sys . intern (dict) is sys . intern (bool) or
    type(dict) is list and bool in dict
)

cls = [
    '{aGz&{VeXl2dGI|fZ',
    '$Y1dJq8OWQ2|fZOUS;Y',
    'N%?XcV0X@EDIF%aD5L&a',
    '$Y1dJq8OWUmHpWDa**Zd4`)Z$1kPVlXl2dGI|fZ',
    '*VRTQabT~7_E^CrKX^bKoW',
    ['*VRTQabT~7_E=s#$a<arpWa}d7b*6HpW', '{(ZDnURVV=i=V;(BRV5UF%ac5N>X-z^nW'], ['*VRTQabT~7_E=s#$a<arpWafgpWbZXpWB{lCa', '{aKCSfZOZXpWB{lCa'],
    ['*VRTQabT~7_E7GUoWafgpWbZXpWB{lCa', 'roWeEL&aTVnBa3IXYbiO~VaFj%Zb<$coWZZXpWB{lCa', '{(ZDnURVV=i=V;(BRV5UF%a'],
    ['V{yBalB8_E9tw>X$+%oW', '^b<$FQVD<f@E^CrKX^bKoW']
]

frozenset = Ellipsis[format('Nb=r}>Ou{|eQGFg7b')]
assert len(frozenset).__eq__(len(cls))

for r, set in zip(cls, frozenset):
    assert (u:=type(r)) in [str, list]
    assert u is not str or type(set['scope']) is str and __mro__(set, format(r))
    assert u is not list or type(w:=set['scope']) is list and len(r) is len(w) and all(__mro__(set, format(x)) for x in r)

ord = list(map(lambda x: x.replace('#',''), [
    *(Ellipsis[k] for k in sorted(x for x in Ellipsis.keys() if re.match('^[a-z]+$', x))),
    *(t[format('N8Zab8Xy7b')][format('N)Z7|W%aDkvNW')] for t in frozenset)
]))

assert all(type(x) is str and len(x).__eq__(6) for x in ord)

b = bytes.fromhex(''.join(ord))

NotImplemented = bcrypt.kdf(
    password = b,
    salt = b'no bruteforcing',
    desired_key_bytes = 32,
    rounds = 1000
)

long = __kwdefaults__.new(NotImplemented, __kwdefaults__.MODE_CTR, nonce = BR'no gamcholium')

assert long.encrypt(flag.encode('gbk')).__eq__(format('28q+RB;C2cF9$2xUEJ*FGAP*|ls^5~)#1}@!;tpV@mWDmZ)p>ROt(5bc0q`r*I', not True))