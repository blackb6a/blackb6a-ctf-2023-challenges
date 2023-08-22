"""
As every bit of the state and it's extracted number is having linear relationship, we can generate a equation
XM = Y, where X is the corresponding state bit, M is a matrix and Y is the extracted bit.
We are going to find the matrix M and store it locally.
"""

from mt19937_64 import MT19937_64
from tqdm import tqdm
import os

length = 19968

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

def gen_row():
    rng = MT19937_64(0)
    g_state = list_state()

    for i in range(length):
        state = next(g_state)
        rng.setstate(state)

        rng.twist()
        row = rng.getstate()[:-1]
        row_bytes = b''.join(b.to_bytes(8, byteorder = 'big') for b in row)

        yield row_bytes


def store_matrix():
    g_row = gen_row()
    f = open(f'mt19937_64_matrix_fast_twist', 'wb')
    for i in tqdm(range(length)):
        row_bytes = next(g_row)
        f.write(row_bytes)
    f.close()


store_matrix()