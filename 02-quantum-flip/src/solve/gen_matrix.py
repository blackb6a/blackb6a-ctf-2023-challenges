#!/usr/bin/pypy3
"""
As every bit of the state and it's extracted number is having linear relationship, we can generate a equation
XM = Y, where X is the corresponding state bit, M is a matrix and Y is the extracted bit.
We are going to find the matrix M and store it locally.
"""

from mt19937_64 import MT19937_64
from tqdm import tqdm
import os

seq_per_file = 3
length = 19968
skip = os.path.getsize('./flag') * 8 - length

def list_state():
    state = [0] * 312
    i = 0
    while i < length:
        index = i // 64
        exponent = i % 64
        state[index] = 1 << (63 - exponent)
        s = state + [0]
        yield s
        state[index] = 0
        i += 1

"""
def get_fast_twist(twist_n):
    M = matrix(GF(2), length, length)
    print("Loading fast twist matrix...")
    with open('mt19937_64_matrix_fast_twist', 'rb') as f:
        for row in tqdm(range(length)):
            bit_arr = bitarray()
            bit_arr.fromfile(f, length//8)
            M[row] = bit_arr.tolist()
    
    t = matrix.identity(GF(2), 19968)
    while (twist_n > 0):
        if twist_n % 2 != 0: t *= M
        M *= M
        twist_n //= 2
    print("Exponential Done!")

    return M

fast_twist_mat = (-1, None)

def fast_skip(rng, n):
    global fast_twist_mat

    twist_n, r = divmod(n, 312)

    if fast_twist_mat[0] != twist_n:
        fast_twist_mat = (twist_n, get_fast_twist(twist_n))
    
    cur_state = ''.join(format(b, '064b') for b in rng.mt)
    cur_vec = vector(GF(2), list(map(int, cur_state)))
    
    new_vec = cur_vec * fast_twist_mat[1]
    
    x = ''.join([str(i) for i in new_vec])
    state = []
    for i in range(312):
        state_i = int(x[i*64:(i+1)*64], 2)
        state.append(state_i)
    rng.mt = state
    
    if r + rng.mti > 312:
        rng.twist()
        rng.mti = (r + rng.mti) % 312
    else:
        rng.mti = r + rng.mti
"""

def gen_row():
    rng = MT19937_64(0)
    g_state = list_state()

    for i in range(length):
        state = next(g_state)
        rng.setstate(state)

        #In this chal, it's using MSB so getrandbits(1)
        row_bytes = [0 for _ in range(0, length, 8)]
        for _ in range(seq_per_file):
            row_bytes = [sum([rng.getrandbits(1) << (7 - k) for k in range(8)]) ^ b for b in row_bytes]
            rng.skip_state(skip)

        yield bytes(row_bytes)


def store_matrix():
    g_row = gen_row()
    f = open(f'mt19937_64_matrix_skip_{skip}', 'wb')
    for i in tqdm(range(length)):
        row_bytes = next(g_row)
        f.write(row_bytes)
    f.close()


store_matrix()