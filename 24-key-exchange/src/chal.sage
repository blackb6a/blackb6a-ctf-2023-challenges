import hashlib
from functools import cache
from secrets import randbelow

def _random_matrix(K, n):
    return Matrix(K, n, [K.from_integer(randbelow(K.order())) for _ in range(n^2)])

def hash_matrix(M):
    s = [ZZ(list(c), 2) for row in M for c in row]
    return hashlib.sha512(str(s).encode()).digest()

def dump_matrix(M):
    return [f.to_integer() for f in M.list()]

n = 512
q = 2^15
K.<x> = GF(q)
A, B = [_random_matrix(K, n) for _ in range(2)]
assert A * B != B * A

class Player:
    @cache
    def fa(self): return A^self.k1
    @cache
    def fb(self): return B^self.k2
    def __init__(self): self.k1, self.k2 = [ZZ(randbelow(2^64)) for _ in range(2)]
    def pub(self): return self.fa() * self.fb()
    def secret(self): return (self.k1, self.k2)
    def exchange(self, recv): self.recv = recv
    def shared(self): return self.fa() * self.recv * self.fb()

print("computing omg")
Alice, Bob = [Player() for _ in range(2)]
Alice.exchange(Bob.pub())
Bob.exchange(Alice.pub())
assert Alice.shared() == Bob.shared()

with open("flag.txt", "r") as fin, open("output.txt", "w") as fout:
    FLAG = fin.read().strip().encode("utf-16")
    assert len(FLAG) <= 64
    enc_FLAG = bytes([x.__xor__(y) for x, y in zip(FLAG, hash_matrix(Alice.shared()))])

    print(K.modulus(), file=fout)
    print(dump_matrix(A), file=fout)
    print(dump_matrix(B), file=fout)
    print(dump_matrix(Alice.pub()), file=fout)
    print(dump_matrix(Bob.pub()), file=fout)
    print(enc_FLAG.hex(), file=fout)
