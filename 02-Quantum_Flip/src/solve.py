from pwn import *
from tqdm import tqdm
from mt19937_64 import MT19937_64
from predict import reverse_state, get_state0

def get_leak(leak, r):
    print("Getting leak...")
    for i in tqdm(range(19968)):
        r.recvuntil(b': ')
        r.sendline(b'0')
        bit = int(r.recvuntil(b'\n', drop=True) == b'Wrong!')
        r.recvuntil(b'\n\n')
        leak.append(bit)

def main():
    while True:
        r = remote('0.0.0.0', 7777)
        leak = []
        get_leak(leak, r)

        rev_state = reverse_state(leak)
        get_state0(leak, rev_state)

        rng = MT19937_64(0)
        rng.setstate(rev_state + [0])

        for i in range(19968):
            rng.getrandbits(1)

        for i in range(100000 - 19968):
            rng_bit = rng.getrandbits(1)
            r.sendline(str(rng_bit))
            res = r.recvuntil(b'\n\n')
            print(res)
            if b'flag' in res:
                break
        else:
            continue
        break

main()