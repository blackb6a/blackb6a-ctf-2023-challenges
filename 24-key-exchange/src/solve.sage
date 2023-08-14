import re
import secrets
import hashlib
from tqdm import tqdm, trange
from functools import cache

def _random_matrix(K, n):
    return Matrix(K, n, [K.from_integer(secrets.randbelow(K.order())) for _ in range(n**2)])

def hash_matrix(M):
    s = [ZZ(list(c), 2) for row in M for c in row]
    return hashlib.sha512(str(s).encode()).digest()

def load_matrix(fin, n):
    nums = list(map(ZZ, fin.readline().strip()[1:-1].split(", ")))
    assert len(nums) == n**2
    nums = [K.from_integer(f) for f in nums]
    return Matrix(K, n, n, nums)

n = 512
q = 2**15

with open("output.txt", "r") as fin:
    # Modulus
    x = var("x")
    modulus = eval(fin.readline().replace("^", "**"))
    K, x = GF(q, modulus=modulus, names="x").objgen()
    print(K, K.modulus())

    A = load_matrix(fin, n)
    B = load_matrix(fin, n)
    A_pub = load_matrix(fin, n)
    B_pub = load_matrix(fin, n)
    enc_FLAG = bytes.fromhex(fin.readline().strip())

vecs = []
ID = Matrix.identity(K, n)

IA = ID
indices = sample(list(range(n**2)), 4*n)
for _ in trange(n):
    lst = IA.list()
    vecs.append([lst[idx] for idx in indices])
    IA *= A

IB = ID
IB_mod = B_pub
for _ in trange(n):
    lst = IB_mod.list()
    vecs.append([lst[idx] for idx in indices])
    IB *= B
    IB_mod *= B

mat = Matrix(K, vecs).transpose()
ker = mat.right_kernel()
assert ker.dimension() >= 1

print("Finding kernel...")
sol = ker.basis()[0]

print("Reconstructing solution!")
A_rec = Matrix.zero(K, n, n)
for s in tqdm(reversed(sol[:n])):
    A_rec = A_rec * A + s * ID

B_rec = Matrix.zero(K, n, n)
for s in tqdm(reversed(sol[n:2 * n])):
    B_rec = B_rec * B + s * ID
B_rec = 1 / B_rec

assert A_rec * B_rec == B_pub
recovered = A_rec * A_pub * B_rec

print("Decryting flag!")
hashed = hash_matrix(recovered)
FLAG = bytes([x.__xor__(y) for x, y in zip(enc_FLAG, hashed)])
print(FLAG.decode("utf-16"))
