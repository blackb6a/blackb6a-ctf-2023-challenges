"""
As every bit of the state and it's extracted number is having linear relationship, we can generate a equation
XM = Y, where X is the corresponding state bit, M is a matrix and Y is the extracted bit.
We are going to find the matrix M and store it locally.
"""

from mt19937_64 import MT19937_64
from tqdm import tqdm

length = 19968
skip = 40000

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

        #In this chal, it's using MSB so getrandbits(1)
        row_bytes1 = [sum([rng.getrandbits(1) << (7 - k) for k in range(8)]) for j in range(0, length, 8)]
        rng.skip_state(skip)
        row_bytes2 = [sum([rng.getrandbits(1) << (7 - k) for k in range(8)]) ^ b for b in row_bytes1]

        yield bytes(row_bytes2)


def store_matrix():
    g_row = gen_row()
    f = open(f'mt19937_64_matrix_skip_{skip}', 'wb')
    for i in tqdm(range(length)):
        row_bytes = next(g_row)
        f.write(row_bytes)
    f.close()


store_matrix()