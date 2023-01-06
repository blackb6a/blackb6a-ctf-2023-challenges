import re
import glob
import hashlib
from tqdm import tqdm, trange

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

EMPTY = set()
state = None

def add(v1, v2):
    return [x ^^ y for x, y in zip(v1, v2)]

def int64_to_vec(x):
    return vector(GF(2), [(x >> i) & 1 for i in range(64)])

def vec_to_int64(x):
    return sum(ZZ(x.get(i)) << i for i in range(64))

def _lshift_vec(vec, k):
    return [EMPTY] * k + list(vec)[:-k]

def _rshift_vec(vec, k):
    return list(vec)[k:] + [EMPTY] * k

def _mask_mask(vec, mask):
    _mask = int64_to_vec(mask)
    return [vec[i] if k else EMPTY for i, k in enumerate(_mask)]

def _mask_const(term, const):
    _mask = int64_to_vec(const)
    return [term if k else EMPTY for k in _mask]

def _process_vec(y):
    y = add(y, _mask_mask(_rshift_vec(y, 29), 0x5555555555555555))
    y = add(y, _mask_mask(_lshift_vec(y, 17), 0x71d67fffeda60000))
    y = add(y, _mask_mask(_lshift_vec(y, 37), 0xfff7eee000000000))
    y = add(y, _rshift_vec(y, 43))
    return y

def AES_decrypt(key, iv, ct):
    key = hashlib.md5(key).digest()
    iv = hashlib.md5(iv).digest()
    cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
    msg = cipher.decrypt(ct)
    try:
        return unpad(msg, 16).decode()
    except ValueError:
        return

const = 0xb5026f5aa96619e9

def twist():
    global state
    print("[+] twist()", flush=True)
    for i in range(312):
        # print("[*]", state[i], state[(i + 1) % 312], flush=True)
        # y = _mask_mask(state[(i + 1) % 312], lower) + _mask_mask(state[i], upper)
        state[i] = state[(i + 1) % 312][1:31] + state[i][31:] + [EMPTY]
        state[i] = add(state[i], state[(i + 156) % 312])
        state[i] = add(state[i], _mask_const(state[(i + 1) % 312][0], const))

### Solve Script

print("Loading data", flush=True)
with open("public/output.txt", "r") as fin:
    ct = bytes.fromhex(fin.readline().split(" = ")[1].strip())
    iv = bytes.fromhex(fin.readline().split(" = ")[1].strip())
    _iv = int.from_bytes(iv, "big")
bits = [None] * 64 + list(map(int, bin(_iv)[2:].zfill(20000 - 64)[::-1]))
print("bits:", bits[:100], flush=True)

print("Initialising variables", flush=True)
state = [[{i * 64 + j} for j in range(64)] for i in range(312)]

res_mat = Matrix(GF(2), 64, 312 * 64)
coef_mat = Matrix(GF(2), len(bits) - 64, 312 * 64)
rhs = vector(GF(2), len(bits) - 64, bits[64:])

print("Calculating coefficients", flush=True)
idx = 0
for i in range(len(bits)):
# for i in range(1000):
    if idx == 0:
        twist()

    y = state[idx]
    idx = (idx + 1) % 312

    y = _process_vec(y)
    msb = y[63]

    if bits[i] is not None:
        # calculated = sum(correct_coef[k] for k in msb) % 2
        # print(f"[{i:<5}]", calculated, "==", bits[i], flush=True)
        # assert calculated == bits[i]

        if idx == 0:
            msb_s = str(msb)
            print(f"[{i:<5}] {msb_s[:20]}...{msb_s[-20:]} == {bits[i]}", flush=True)
    
    if bits[i] is not None:
        # extract coefficients from msb
        for k in msb:
            coef_mat[i - 64, k] = 1
    else:
        for k in msb:
            res_mat[i, k] = 1

print("Done!", flush=True)

print("Started solving equations...", flush=True)

res = coef_mat.solve_right(rhs)
print("solution:", res, flush=True)

ker = coef_mat.right_kernel()
print("kernel:", ker, flush=True)

print(coef_mat.dimensions(), flush=True)

basis = ker.basis()
for vec in basis:
    s = ''.join(map(str, vec))
    print(s[:20], s[-20:], s.count('1'), flush=True)

required = set()
for vec in res_mat:
    for idx in range(312 * 64):
        if vec[idx] == 1:
            required.add(idx)

for vec in res_mat:
    print([idx for idx in range(312 * 64) if vec[idx] == 1], flush=True)

basis = list(basis)
basis = [vec for vec in basis if len(set(idx for idx in range(len(vec)) if vec[idx]) & required) > 0]
for vec in basis:
    s = ''.join(map(str, vec))
    print(s[:20], s[-20:], s.count('1'), flush=True)

for _null in span(basis):
    _sol = res + _null
    _recovered = res_mat * _sol
    key = ''.join(map(str, _recovered))[::-1]
    key = int(key, 2).to_bytes(len(key) // 8, 'big')
    print(AES_decrypt(key, iv, ct), flush=True)




