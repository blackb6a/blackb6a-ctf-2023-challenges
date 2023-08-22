from mt19937_64 import MT19937_64
from bitarray import bitarray
from tqdm import tqdm
from sage.all import *

MATRIX_FILE = 'mt19937_64_matrix'
length = 19968

def load_matrix():
    m = matrix(GF(2), length, length)
    print("Loading matrix...")
    with open(MATRIX_FILE, 'rb') as f:
        for row in tqdm(range(length)):
            bit_arr = bitarray()
            bit_arr.fromfile(f, length//8)
            m[row] = bit_arr.tolist()
    return m

m = load_matrix()

#Solve the linear equations
def reverse_state(leak):
    print("Solving linear relationship...")
    x = m.solve_left(vector(GF(2), leak))
    x = ''.join([str(i) for i in x])
    state = []
    for i in range(312):
        state_i = int(x[i*64:(i+1)*64], 2)
        state.append(state_i)
    return state

#As the matrix is not full rank, we need to guess 32 bits of the state bits.
#This could be done by using the state[311] it contains the information of least 31 bits of state[0]
def get_state0(leak, state):
    low = 0x7FFFFFFF
    mask = 0xB5026F5AA96619E9
    tmp = state[311] ^ state[155]
    if tmp >> 63 == 1:
        tmp ^= mask
        tmp <<= 1
        tmp += 1
    else:
        tmp <<= 1
		
    guess = [tmp & low | (1 << 31), tmp & low]
    rng = MT19937_64(0)
    
    state[0] &= 0xFFFFFFFF00000000
    state[0] |= guess[0]
    rng.setstate(state + [0])
    
    guess_result = [rng.getrandbits(1) for _ in range(length)]
    if guess_result == leak:
        return
    
    state[0] &= 0xFFFFFFFF00000000
    state[0] |= guess[1]
    rng.setstate(state + [0])
    
    guess_result = [rng.getrandbits(1) for _ in range(length)]
    if guess_result == leak:
        return
    
    raise Exception("No state 0 found!")


#Showcase
def get_leak():
    rng = MT19937_64(0)
    prefix = [rng.getrandbits(1) for _ in range(100)]
    leak = [rng.getrandbits(1) for _ in range(length)]
    to_predict = [rng.getrandbits(1) for _ in range(length*3)]
    return leak, prefix, to_predict

def main():
    leak, prefix, ans = get_leak()
    rev_state = reverse_state(leak)
    get_state0(leak, rev_state)

    rng = MT19937_64(0)
    rng.setstate(rev_state + [0])

    predict_prefix = [rng.getrandbits(1, reverse = True) for _ in range(100)][::-1]; [rng.getrandbits(1) for _ in range(100)]
    leaked = [rng.getrandbits(1) for _ in range(length)]
    predict = [rng.getrandbits(1) for _ in range(length*3)]

    print(predict == ans)
    print(predict_prefix == prefix)

if __name__ == '__main__':
    main()
