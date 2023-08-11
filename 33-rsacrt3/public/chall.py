import os
from Crypto.Random import random
from Crypto.Cipher import AES
import json

class PRNG1:
    def __init__(self, p, a, c, seed):
        self.p = p
        self.a = a
        self.c = c
        self.x = seed

    def next(self):
        a, c, x, p = self.a, self.c, self.x, self.p
        self.x = (a * x + c) % p
        return self.x


class PRNG2:
    def __init__(self, seed):
        self.x = seed

    def next(self):
        pt = self.x.to_bytes(16, 'big')
        cipher = AES.new(b'BauhiniaCTFFTW!!', AES.MODE_ECB)
        ct = cipher.encrypt(pt)
        self.x = int.from_bytes(ct, 'big')
        return self.x


def main():
    flag = os.environb.get(b'FLAG', b'b6actf{this_is_a_fake_flag}')
    flag += b'\0' * (128-len(flag))
    assert len(flag) == 128

    # Defining the first PRNG
    # Note: p is slightly greater than 2^128 to ensure 128 bit output
    p = 0x100720f648a7a4c0a305489880973cf45
    a = random.getrandbits(128)
    c = random.getrandbits(128)
    key1 = random.getrandbits(128)
    prng1 = PRNG1(p, a, c, key1)

    # Defining the second PRNG
    key2 = random.getrandbits(128)
    prng2 = PRNG2(key2)

    # Encrypting the flag
    for k in [key1, key2]:
        cipher = AES.new(k.to_bytes(16, 'big'), AES.MODE_ECB)
        flag = cipher.encrypt(flag)

    # Who doesn't love leaks?
    leaks = [prng1.next() ^ prng2.next() for _ in range(16384)]

    print(json.dumps({
        "prng1": {"p": p, "a": a, "c": c},
        "prng2": {},
        "flag": flag.hex(),
        "leaks": leaks
    }))

if __name__ == '__main__':
    main()
