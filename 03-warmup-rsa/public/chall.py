from math import gcd, lcm
from Crypto.Util.number import getPrime, getRandomNBitInteger, bytes_to_long
from secret import flag

bits = 1024
given = bits // 5
e_bits = bits // 12

mask = (1 << given) - 1

while True:
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    N = p * q

    if N.bit_length() != bits:
        continue

    l = lcm(p - 1, q - 1)
    e = getRandomNBitInteger(e_bits)

    if gcd(e, l) > 1:
        continue

    d = pow(e, -1, l)

    dp = int(d % (p - 1))
    dq = int(d % (q - 1))

    break

l_dp = dp & mask
l_dq = dq & mask

print(f'{N = }')
print(f'{e = }')
print(f'{l_dp = }')
print(f'{l_dq = }')

# RSA encryption, -1 because of flag format
flag = bytes_to_long(flag)

assert flag.bit_length() == bits - 1 and flag < N

ct = pow(flag, e, N)
print(f'{ct = }')