# This challenge was inspired by the RSALCG2 in zer0pts CTF 2023.
#
# Notably, the above line is copied from its challenge description (and modified
# slightly to make it more original).
# To keymoon: If you see the challenge, please don't sue me :)
#                                                                       - Mystiz

import os
import random
import dataclasses

from Crypto.Hash import SHA256
from Crypto.Util.number import isPrime, getRandomInteger

FLAG = os.getenv("FLAG", "b6actf{*** REDACTED ***}")
SEED = SHA256.new(FLAG.encode()).digest()
while len(SEED) < 623 * 4:
  SEED += SHA256.new(SEED).digest()
random.seed(SEED)

# TODO: change this back to rsactf2's setting
def randbytes(x):
  return int.to_bytes(random.getrandbits(x*8), x, 'big')

def deterministicGetPrime(bits):
  # ...of course I have to inject something (seemingly) vulnerable :)
  while True:
    p = 2**(bits-1) + getRandomInteger(bits-10, randfunc=randbytes)
    if isPrime(p): return p

def deterministicGetRandomInteger(bits):
  return getRandomInteger(bits, randfunc=randbytes)

@dataclasses.dataclass
class RSALCG:
  a: int
  b: int
  e: int
  n: int
  s: int
  def next(self):
    self.s = (self.a * self.s + self.b) % self.n
    return pow(self.s, e, n)

def decrypt(rands, msg):
  assert len(msg) <= 128
  m = int.from_bytes(msg, "big")
  for rand in rands:
    res = rand.next()
    m ^= res
    print(f"debug: {m}")
    m ^= rand.s
  return m.to_bytes(128, "big")

ROUND = 30

a = deterministicGetRandomInteger(1024)
b = deterministicGetRandomInteger(1024)
e = 2**84 + 3 # I am making e super large so you can't feasibly do HGCD :)
n = deterministicGetPrime(512) * deterministicGetPrime(512)
print(f"{a = }")
print(f"{b = }")
print(f"{e = }")
print(f"{n = }")

# ATTENTION: s is deterministic! But so what? You don't have `nc` anyways.
rands = [RSALCG(a, b, e, n, deterministicGetRandomInteger(1024) % n) for _ in range(ROUND)]

while True:
  m = decrypt(rands, bytes.fromhex(input("> ")))
  if m.lstrip(b"\x00") == FLAG.encode():
    print(f"Your flag is correct!")
  else:
    print("I couldn't understand what you meant...")
