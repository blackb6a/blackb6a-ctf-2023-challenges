import secrets
import hashlib
from functools import cache

def _random_matrix(K, n):
    return Matrix(K, n, [K.from_integer(secrets.randbelow(K.order())) for _ in range(n^2)])

def hash_matrix(M):
    s = [ZZ(list(c), 2) for row in M for c in row]
    return hashlib.sha512(str(s).encode()).digest()
    
n = 256
q = 2^13
K = GF(q)
A, B = [_random_matrix(K, n) for _ in range(2)]
assert A * B != B * A

class Player:
    def __init__(self): self.k1, self.k2 = [ZZ(secrets.randbelow(2^64)) for _ in range(2)]
    def pub(self): return A^self.k1 * B^self.k2
    def secret(self): return (self.k1, self.k2)
    def exchange(self, recv): self.recv = recv
    def shared(self): return A^self.k1 * self.recv * B^self.k2

Alice, Bob = [Player() for _ in range(2)]
Alice.exchange(Bob.pub())
Bob.exchange(Alice.pub())
assert Alice.shared() == Bob.shared()

with open("flag.txt", "r") as fin, open("output.txt", "w") as fout:
    FLAG = fin.read().strip().encode("utf-16")
    assert len(FLAG) <= 64
    enc_FLAG = bytes([x.__xor__(y) for x, y in zip(FLAG, hash_matrix(Alice.shared()))])
    
    print(K.modulus(), file=fout)
    print(A, file=fout)
    print(B, file=fout)
    print(Alice.pub(), file=fout)
    print(Bob.pub(), file=fout)
