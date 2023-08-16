def _int64(x):
    return int(0xFFFFFFFFFFFFFFFF & x)

#A python version of mt19937_64
class MT19937_64:
    def __init__(self, seed):
        self.mt = [0] * 312
        self.mt[0] = seed
        self.mti = 312
        for i in range(1, 312):
            self.mt[i] = _int64(6364136223846793005 * (self.mt[i - 1] ^ self.mt[i - 1] >> 62) + i)


    def extract_number(self, reverse):
        if not reverse:
            if self.mti == 312:
                self.twist()
                self.mti = 0
        else:
            if self.mti == 0:
                self.backtrace()
                self.mti = 312

        if reverse:
            self.mti = self.mti - 1

        y = self.mt[self.mti]
        y = y ^ y >> 29 & 0x5555555555555555
        y = y ^ y << 17 & 0x71D67FFFEDA60000
        y = y ^ y << 37 & 0xFFF7EEE000000000
        y = y ^ y >> 43
        
        if not reverse:
            self.mti = self.mti + 1

        return _int64(y)

    def backtrace(self):
        high = 0xFFFFFFFF80000000
        low = 0x7FFFFFFF
        mask = 0xB5026F5AA96619E9
        for i in range(311, -1, -1):
            tmp = self.mt[i] ^ self.mt[(i + 156) % 312]
            if tmp >> 63 == 1:
                tmp ^= mask
                tmp <<= 1
                tmp |= 1
            else:
                tmp <<= 1
            res = tmp & high
            tmp = self.mt[i-1] ^ self.mt[(i + 155) % 312]
            if tmp >> 63 == 1:
                tmp ^= mask
                tmp <<= 1
                tmp |= 1
            else:
                tmp <<=1
            res |= tmp & low
            self.mt[i] = res
    
    def skip_state(self, n):
        twist_n, r = divmod(n, 312)
        for _ in range(twist_n):
            self.twist()
        if r + self.mti > 312:
            self.twist()
            self.mti = (r + self.mti) % 312
        else:
            self.mti = r + self.mti

    def twist(self):
        for i in range(312):
            y = _int64((self.mt[i] & 0xFFFFFFFF80000000) + (self.mt[(i + 1) % 312] & 0x7fffffff))
            self.mt[i] = (y >> 1) ^ self.mt[(i + 156) % 312]

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0xB5026F5AA96619E9
    
    def getrandbits(self, bits, reverse = False):
        assert bits > 0 and bits <= 64
        return self.extract_number(reverse) >> (64 - bits)
    
    def setstate(self, mt_mti):
        assert len(mt_mti) == 313
        self.mt = mt_mti[:-1]
        self.mti = mt_mti[-1]

    def getstate(self):
        return self.mt + [self.mti]

#In qiskit random, it's actually using mt19937_64 discrete_distribution, which is the following function (there are some modification in here)
#It's actually the same thing as getrandbits(1) (unless the extracted number is 2^63, won't be that unlucky right?)
def discrete_distribution(probs, rng):
    assert len(probs) == 2 and probs[0] + probs[1] == 1
    
    threshold = rng.extract_number() / 2**64
    return int(probs[0] < threshold)