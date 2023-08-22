from bitarray import bitarray
from tqdm import tqdm
import os
from mt19937_64 import MT19937_64
from predict import reverse_state, get_state0

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

    leak = get_leak_vector()
    rev_state = reverse_state(leak)
    get_state0(leak, rev_state)

    rng = MT19937_64(0)
    rng.setstate(rev_state + [0])

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

if __name__ == '__main__':
    main()