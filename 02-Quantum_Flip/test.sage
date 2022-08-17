from tqdm import trange

n = 5000

_coef = pari(f"matrix({n},{n},i,j,random([0,1]))")
_state = pari(f"vectorv({n},i,random([0,1]))")

_rhs = _coef * _state
for i in trange(n):
    _rhs[i] = ZZ(_rhs[i] % 2)

print(_rhs)
print("Recovering")

_res = pari.matsolvemod(_coef, 2, _rhs)
print("Recovered:", _res)