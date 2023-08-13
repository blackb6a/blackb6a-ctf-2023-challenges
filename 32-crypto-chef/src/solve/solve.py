import galois
import numpy as np
import itertools
from pwn import *

from PoW import PoW_solve

context.log_level = 'debug'
#r = process(['/bin/bash', './chall/start.sh'])
r = remote('localhost', 30032)

k = 4
q = 2**k
o = 16
v = 16
n = o + v

WATER_TAP = [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1]

class LFSR:
    def __init__(self, taps, seed):
        self.state = seed[:]
        self.taps = vector(GF(2), taps[::-1])

    def next(self):
        out = self.taps * vector(GF(2), self.state)
        self.state.pop(0)
        self.state.append(out)
        return int(out)

    def next_salt(self):
        salt = [0 for _ in range(8)]
        for i, j in itertools.product(range(8), range(4)):
            salt[i] <<= 1
            salt[i] |= self.next()
        return salt

class LFSRSalt:
    def __init__(self, q, water_tap, salt):
        self.GF = galois.GF(2)
        self.q = q
        self.k = self.q.bit_length() - 1
        assert self.q == 2**self.k

        self.lfsr = galois.FLFSR.Taps(self.GF(water_tap), self.GF([(c >> (self.k - i - 1)) & 1 for c in salt.view(np.ndarray) for i in range(self.k)][::-1]))
        self.step(len(water_tap) // self.k)
    
    def step(self, num):
        rtn = []
        for _ in range(num):
            elem = 0
            for _ in range(self.k):
                elem <<= 1
                elem |= int(self.lfsr.step(1))
            rtn.append(elem)

        return galois.GF(self.q)(rtn)

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

def getPub():
    r.recvuntil(b'> ')
    r.sendline(b'pub')
    r.recvuntil(b'Recipe 2: ')

    pub_str = r.recvuntil(b'\n', drop=True).decode()
    const, lin, quad = pub_str.split(':')

    const = galois.GF(16)([int(c, 16) for c in const])
    lin = galois.GF(16)([int(c, 16) for c in lin])
    quad = galois.GF(16)([int(c, 16) for c in quad])

    const = const.reshape((o,))
    lin = lin.reshape((o, n))
    quad = quad.reshape((o, n, n))

    return const, lin, quad

def sign(recipe, msg):
    msg = vec2Hex(msg)
    r.recvuntil(b'> ')
    r.sendline(f'cook {recipe} {msg}'.encode())
    r.recvuntil(b': ')

    res = r.recvuntil(b'\n', drop=True).decode()
    return galois.GF(16)([int(c, 16) for c in res])

def verify(recipe, sign, msg):
    sign = vec2Hex(sign)
    msg = vec2Hex(msg)
    r.recvuntil(b'> ')
    r.sendline(f'check {recipe} {sign} {msg}'.encode())

def sendAns(recipe, ans):
    ans = vec2Hex(ans)
    r.recvuntil(b'> ')
    r.sendline(f'exam {recipe} {ans}'.encode())

def getOilBasis(pub_quad):

    gGF = galois.GF(16)

    nonSingularG = []
    for i in range(o):
        if np.linalg.matrix_rank(pub_quad[i]) < n:
            continue
        nonSingularG.append(pub_quad[i])

    G_len = len(nonSingularG)
    closureT = gGF.Zeros((G_len**2, n**2))
    for i in range(G_len):
        for j in range(G_len):
            G_ij = np.linalg.inv(nonSingularG[i]) @ nonSingularG[j]
            closureT[i*G_len + j] = G_ij.flatten()
    
    closureT = closureT.row_reduce()
    idx = np.argwhere(np.all(closureT[..., :] == 0, axis=1))
    closureT = np.delete(closureT, idx, axis=0)
    closureT = closureT.reshape((-1, n, n))

    R = None
    prev_rank = 0
    offset = 0
    while True:
        M = gGF.Zeros((n, n))
        for i in range(offset, offset + o):
            M += gGF.Random(1) * closureT[i]
        M -= closureT[offset + o]

        r = M.null_space()
        if len(r) > 0:
            r = r[0]
            r = np.expand_dims(r, axis = 0)
            if R is None:
                R = r
            else:
                R = np.concatenate((R, r), axis = 0)
            
            rank = np.linalg.matrix_rank(R)
            prev_rank = rank

            if rank == o:
                break

            if prev_rank == rank:
                offset += 1

    R = gGF(R.row_reduce()[:o])
    return R

def findOil(F, vinegar, msg):

    A = galois.GF(16).Zeros((16, 16))
    b = msg.copy()

    for i in range(16):

        quadOil = np.sum((F[2][i][:16, -16:] + F[2][i].transpose()[:16, -16:]) * vinegar, axis = 1)
        quadConst = vinegar @ F[2][i][-16:, -16:] @ vinegar

        linOil = F[1][i][:16]
        linConst = F[1][i][-16:] @ vinegar

        A[i] = quadOil + linOil
        b[i] -= quadConst + linConst + F[0][i]
    
    if np.linalg.matrix_rank(A) < 16:
        return None
    
    return np.linalg.solve(A, b)

def debugGetA():
    A = galois.GF(16).Zeros((32, 32))
    for i in range(32):
        A[i] = sign(1, galois.GF(16).Identity(32)[i])
    return A.T

def main():

    solvePoW()

    const, lin, quad = getPub()
    R = getOilBasis(quad)

    reg_R = galois.GF(16).Zeros((16, 32))
    for i in range(len(R)):
        reg_R[i] = sign(1, R[i])
    
    assert np.all(reg_R.row_reduce()[0][16:] == 0)

    # Find invertible square mat of reg_R.T
    reg_R_T = reg_R.T[0:1]
    for i in range(len(reg_R.T)):
        tmp = np.concatenate((reg_R_T, reg_R.T[i:i+1]))
        if np.linalg.matrix_rank(tmp) == len(tmp):
            reg_R_T = tmp

    B1 = R.T @ np.linalg.solve(reg_R_T, galois.GF(16).Identity(16))
    B1 = B1.T

    B = galois.GF(16).Zeros((9, 32))
    A = galois.GF(16).Zeros((9, 9))
    for i in range(9):
        x = sign(2, galois.GF(16).Random(16))
        ax = sign(1, x)

        oil, pepper, salt = ax[0:16], ax[16:24], ax[24:32]
        B[i] = x - B1.T @ oil
        A[i] = np.insert(salt, 0, 1)
    
    S = np.linalg.solve(A, B)
    A_inv_pepper, B3 = S[0], S[1:]

    next_salt = LFSRSalt(16, WATER_TAP, salt).step(8)
    A_inv_vinegar = A_inv_pepper + B3.T @ next_salt

    """
    #### DEBUG ####
    DEBUG_A = debugGetA()

    F = galois.GF(16).Zeros((16, 32, 32))
    for i in range(16):
        F[i] = np.linalg.inv(DEBUG_A).T @ quad[i] @ np.linalg.inv(DEBUG_A)
    
    F_lin = lin @ np.linalg.inv(DEBUG_A)
    #### END ####
    """

    M = np.vstack([R, A_inv_vinegar])
    while np.linalg.matrix_rank(M) < 32:
        rand_basis = galois.GF(16).Random(32)
        if np.linalg.matrix_rank(np.vstack([M, rand_basis])) == len(M) + 1:
            M = np.vstack([M, rand_basis])
    
    forged_quad = galois.GF(16).Zeros((16, 32, 32))
    for i in range(16):
        forged_quad[i] = M @ quad[i] @ M.T
    forged_lin = lin @ M.T
    forged_const = const

    msg2 = galois.GF(16)([int(c, 16) for c in b'ilovemsg'.hex()])
    forged_vinegar = galois.GF(16)([1] + [0] * 15)
    forged_sign = np.append(findOil((forged_const, forged_lin, forged_quad), forged_vinegar, msg2), forged_vinegar)

    ans2 = M.T @ forged_sign
    
    msg1 = galois.GF(16)([int(c, 16) for c in b'cryptochefisgood'.hex()])
    ans1 = ax + sign(1, msg1 - x)
    sendAns(1, ans1)
    sendAns(2, ans2)

    r.interactive()

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