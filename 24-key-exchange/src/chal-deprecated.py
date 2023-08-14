# Accelerated version of chal.sage used to generate data
# Not public (inb4 CTF drama)
# Update: Nevermind this is ~100x slower than Sage
import hashlib
import numpy as np
from galois import GF
from secrets import randbelow
from numpy.linalg import matrix_power as matpow

def _random_matrix(K, n):
    M = np.ndarray([n, n], dtype=K)
    for i in range(n):
        for j in range(n):
            M[i, j] = K(randbelow(K.order))
    return M

def hash_matrix(M):
    s = str(dump_matrix(M))
    return hashlib.sha512(s.encode()).digest()

def dump_matrix(M):
    return [int(f) for f in M.flatten()]

n = 64
q = 2**13
K = GF(q)
A, B = [_random_matrix(K, n) for _ in range(2)]
assert np.any(A @ B != B @ A), "[1] grhkm sucks frfr"

class Player:
    def __init__(self): self.k1, self.k2 = [randbelow(2**64) for _ in range(2)]
    def powA(self): return matpow(A, self.k1)
    def powB(self): return matpow(B, self.k2)
    def pub(self): return self.powA() @ self.powB()
    def secret(self): return (self.k1, self.k2)
    def exchange(self, recv): self.recv = recv
    def shared(self): return self.powA() @ self.recv @ self.powB()

Alice, Bob = [Player() for _ in range(2)]
Alice.exchange(Bob.pub())
Bob.exchange(Alice.pub())
assert np.any(Alice.pub() != Bob.pub()), "[2] grhkm sucks frfr"

with open("flag.txt", "r") as fin, open("output.txt", "w") as fout:
    FLAG = fin.read().strip().encode("utf-16")
    assert len(FLAG) <= 64
    enc_FLAG = bytes([x ^ y for x, y in zip(FLAG, hash_matrix(Alice.shared()))])

    print(str(K.irreducible_poly), file=fout)
    print(dump_matrix(A), file=fout)
    print(dump_matrix(B), file=fout)
    print(dump_matrix(Alice.pub()), file=fout)
    print(dump_matrix(Bob.pub()), file=fout)
    print(enc_FLAG.hex(), file=fout)
