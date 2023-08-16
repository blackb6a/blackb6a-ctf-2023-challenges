from mt19937_64 import MT19937_64
from sage.all import *
from bitarray import bitarray

from tqdm import tqdm

MATRIX_FILE = 'mt19937_64_matrix_fast_twist'
length = 19968

def load_matrix():
    m = matrix(GF(2), length, length)
    print("Loading matrix...")
    with open(MATRIX_FILE, 'rb') as f:
        for row in tqdm(range(length)):
            bit_arr = bitarray()
            bit_arr.fromfile(f, length//8)
            m[row] = bit_arr.tolist()
    print("Matrix rank:", m.rank())
    return m

def state2GF2(rng):
    ori_state = rng.getstate()[:-1]
    ori_state = b''.join(b.to_bytes(8, byteorder = 'big') for b in ori_state)
    a = bitarray()
    a.frombytes(ori_state)
    return vector(GF(2), a.tolist())

m = load_matrix()

rng = MT19937_64(12345678)

test_state = state2GF2(rng) * (m**100)
for _ in range(100):
    rng.twist()
true_state = state2GF2(rng)

print(test_state == true_state)
