from sage.all import *
from sage.matrix.berlekamp_massey import berlekamp_massey

import galois
import numpy as np
from pwn import *

from PoW import PoW_solve

context.log_level = 'debug'
r = remote('chall.pwnable.hk', 30032)

MSG = galois.GF(16).Random(16)

def vec2Hex(vec):
    vec = np.char.mod('%x', vec.view(np.ndarray))
    return ''.join(vec)

def solvePoW():
    r.recvuntil(b':')
    r.recvuntil(b':')
    given = r.recvuntil(b':', drop=True).decode()
    r.recvuntil(b'= ')
    h = r.recvuntil(b'\n', drop=True).decode()

    found = PoW_solve(given, h)

    r.recvuntil(b'> ')
    r.sendline(found.encode())

def sign(recipe, msg):
    msg = vec2Hex(msg)
    r.recvuntil(b'> ')
    r.sendline(f'cook {recipe} {msg}'.encode())
    r.recvuntil(b': ')

    res = r.recvuntil(b'\n', drop=True).decode()
    return galois.GF(16)([int(c, 16) for c in res])

def main():

    solvePoW()

    seq = sign(1, sign(2, MSG))[-8:]
    seq = np.append(seq, sign(1, sign(2, MSG))[-8:])
    seq = np.append(seq, sign(1, sign(2, MSG))[-8:])
    seq = np.append(seq, sign(1, sign(2, MSG))[-8:])

    seq_binary = [(c >> (4 - i - 1)) & 1 for c in seq.view(np.ndarray) for i in range(4)]
    seq_binary[0] = GF(2)(seq_binary[0])
   
    poly = berlekamp_massey(seq_binary)
    res_tap = [0] * 32
    for k in poly.dict().keys():
        if k < 32:
            res_tap[k] = 1

    res_tap = res_tap[::-1]
    print(res_tap)

if __name__ == '__main__':
    main()

"""
water_tap = [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1]

salt = galois.GF(2).Random(32)
lfsr = galois.FLFSR.Taps(galois.GF(2)(water_tap), salt)
salt = salt.view(np.ndarray)

next32 = lfsr.step(32).view(np.ndarray)
next64 = lfsr.step(32).view(np.ndarray)
next96 = lfsr.step(32).view(np.ndarray)

seq = list(np.append(salt, [next32, next64, next96]))
seq[0] = GF(2)(seq[0])

poly = berlekamp_massey(seq)
res_tap = [0] * 32
for k in poly.dict().keys():
    if k < 32:
        res_tap[k] = 1

res_tap = res_tap[::-1]
print(res_tap)
"""