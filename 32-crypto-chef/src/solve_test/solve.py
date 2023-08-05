import galois
import numpy as np
import base64

from OV import OilVinegar
from tqdm import tqdm

WATER_TAP = None

def getPepperOrSalt(q, v):
    return galois.GF(q).Random(v // 2)

def getSause(q, n):
    secret_sause = galois.GF(q).Random((n, n))
    while np.linalg.matrix_rank(secret_sause) < n:
        secret_sause = galois.GF(q).Random((n, n))
    return secret_sause

q = 16
o = 2
v = 2
n = o + v
GF = galois.GF(q)

salt = getPepperOrSalt(q, v)
pepper = getPepperOrSalt(q, v)
secret_sause = getSause(q, n)

ov = OilVinegar(q, o, v, WATER_TAP, salt, pepper, secret_sause)

_, pub = ov.genkey()

pub_const, pub_lin, pub_quad = pub

nonSingularG = []
for i in range(o):
    if np.linalg.matrix_rank(pub_quad[i]) < n:
        continue
    nonSingularG.append(pub_quad[i])

assert len(nonSingularG) == o


closureT = GF.Zeros((o**2, n**2))
for i in tqdm(range(o)):
    for j in range(o):
        G_ij = np.linalg.inv(pub_quad[i]) @ pub_quad[j]
        closureT[i*o + j] = G_ij.flatten()

closureT = closureT.row_reduce()
idx = np.argwhere(np.all(closureT[..., :] == 0, axis=1))
closureT = np.delete(closureT, idx, axis=0)
closureT = closureT.reshape((-1, n, n))

print(closureT)