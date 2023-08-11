import json
from Crypto.Cipher import AES

class PRNG2:
    def __init__(self, seed):
        self.x = seed

    def next(self):
        pt = self.x.to_bytes(16, 'big')
        cipher = AES.new(b'BauhiniaCTFFTW!!', AES.MODE_ECB)
        ct = cipher.encrypt(pt)
        self.x = int.from_bytes(ct, 'big')
        return self.x

with open('output.json') as f: j = json.load(f)

a = j.get('prng1').get('a')
c = j.get('prng1').get('c')
p = j.get('prng1').get('p')
xs = j.get('leaks')
flag = bytes.fromhex(j.get('flag'))

n = len(xs)

ids = [i for i in range(n) if xs[i] >= 2**128]

k = len(ids)
print(f'We will use {ids = }. There are {k = } entries!')

r = (2^128 + p) // 2
weights = [1] + [1/r for _ in range(k)]

A = Matrix(QQ, k+1, k+1)
Q = diagonal_matrix(weights)


if True:
    A[0,   0  ] = 1

    A[0,   1  ] = -r
    A[1,   1  ] = 1
for i in range(1, k):
    A[0,   i+1] = int(c * (pow(a, ids[i]-ids[0], p)-1) * pow(a-1, -1, p) % p) - r
    A[1,   i+1] = int(pow(a, ids[i]-ids[0], p))
    A[i+1, i+1] = p

A *= Q
A = A.LLL()
A /= Q

for row in A:
    if row[0] < 0: row = -row
    if row[0] != 1: continue
    res = [(v+r)%p for v in row[1:]]
    if not all(v>=2^128 for v in res): continue

    x = x1 = int(pow(a, -ids[0], p) * (res[0] - c * (pow(a, ids[0], p)-1) * pow(a-1, -1, p)) % p)
    y = y1 = xs[0] ^^ x
    prng = PRNG2(y)
    for i in range(n):
        if x^^y != xs[i]:
            print(f'Mismatch at {i = }')
            break
        x = (a * x + c) % p
        y = prng.next()
    else:
        # Everything matches!
        x0 = int((x1 - c) * pow(a, -1, p) % p)

        cipher = AES.new(b'BauhiniaCTFFTW!!', AES.MODE_ECB)
        y0 = cipher.decrypt(int(y1).to_bytes(16, 'big'))
        y0 = int.from_bytes(y0, 'big')

        for key in [y0, x0]:
            cipher = AES.new(int(key).to_bytes(16, 'big'), AES.MODE_ECB)
            flag = cipher.decrypt(flag)
        print(f'Solution found! {x0 = }, {flag = }')

        break

