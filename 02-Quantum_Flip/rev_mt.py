from z3 import *
from tqdm import tqdm


def _cast(x):
    return int(0xFFFFFFFFFFFFFFFF & x)


class MT19937_64:

    def __init__(self, seed):
        self.mt = [0] * 312
        self.mt[0] = seed
        self.mti = 0
        for i in range(1, 312):
            self.mt[i] = _cast(6364136223846793005 *
                               (self.mt[i - 1] ^ self.mt[i - 1] >> 62) + i)

    def get(self):
        if self.mti == 0:
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 29 & 0x5555555555555555
        y = y ^ y << 17 & 0x71d67fffeda60000
        y = y ^ y << 37 & 0xfff7eee000000000
        y = y ^ y >> 43
        self.mti = (self.mti + 1) % 312
        return _cast(y)

    def twist(self):
        LOW = (1 << 31) - 1
        HIGH = ((1 << 64) - 1) - ((1 << 31) - 1)
        for i in range(0, 312):
            y = (self.mt[i] & HIGH) | (self.mt[(i + 1) % 312] & LOW)
            self.mt[i] = (y >> 1) ^ self.mt[(i + 156) % 312]

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0xb5026f5aa96619e9
