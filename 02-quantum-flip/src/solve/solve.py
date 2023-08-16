from bitarray import bitarray
from tqdm import tqdm
import os
from mt19937_64 import MT19937_64
from predict import reverse_state, get_state0, get_leak, get_prefix

def get_leak_vector():
    enc_vec = bitarray()
    with open('quantum.jpg.enc', 'rb') as f:
        enc_vec.fromfile(f)
    
    plain_vec = bitarray()
    with open('quantum.jpg', 'rb') as f:
        plain_vec.fromfile(f)
    
    stream_vec = plain_vec ^ enc_vec
    return stream_vec.tolist()[::-1][:19968]

def main():

    pass
    """

    real_leak = get_leak_vector()
    
    rng = MT19937_64(3064954383174244867)
    ans_prefix = get_prefix(rng)
    leak = get_leak(rng)

    debug_stream = bitarray()
    with open('debug_stream', 'rb') as f:
        debug_stream.fromfile(f)

    flag_len = os.path.getsize('./flag.enc') * 8
    debug_stream = debug_stream.tolist()[::-1]

    known_stream = debug_stream[flag_len * 3 : ]
    quantum_len = len(known_stream) // 3
    known_stream_xor = bitarray(known_stream[:quantum_len]) ^ bitarray(known_stream[quantum_len:quantum_len*2]) ^ bitarray(known_stream[quantum_len*2:quantum_len*3])
    known_stream_xor = known_stream_xor.tolist()[:19968]

    print(leak == real_leak) # False
    print(leak == known_stream_xor) # False
    print(real_leak == known_stream_xor) # True

    """


    """

    leak = get_leak_vector()
    rev_state = reverse_state(leak)
    get_state0(leak, rev_state)

    rng = MT19937_64(0)
    rng.setstate(rev_state + [0])

    debug_stream = bitarray()
    with open('debug_stream', 'rb') as f:
        debug_stream.fromfile(f)
    
    flag_len = os.path.getsize('./flag.enc') * 8
    debug_stream = debug_stream.tolist()[::-1]

    known_stream = debug_stream[flag_len * 3 : ]
    my_gen = [rng.getrandbits(1) for _ in range(len(known_stream))]

    """

    """
    flag_len = os.path.getsize('./flag.enc') * 8
    stream = bitarray('0' * flag_len)

    for _ in range(3):
        stream ^= bitarray([rng.getrandbits(1, reverse = True) for _ in range(flag_len)])

    enc_flag = bitarray()
    with open('flag.enc', 'rb') as f:
        enc_flag.fromfile(f)
    
    flag_file = stream ^ enc_flag
    with open('flag', 'wb') as f:
        flag_file.tofile(f)
    """

if __name__ == '__main__':
    main()