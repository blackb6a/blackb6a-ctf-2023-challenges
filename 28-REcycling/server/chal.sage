from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.finite_rings.integer_mod_ring import Integers

x = PolynomialRing(Integers(), "x").0
e = 65537
n = 0x100000000
ct = 2147483648*x**18 + 2684354560*x**17 + 2952790016*x**16 + 1073741824*x**15 + 1073741824*x**14 + 3623878656*x**13 + 2214592512*x**12 + 1275068416*x**11 + 3338665984*x**10 + 1094713344*x**9 + 3579838464*x**8 + 1950351360*x**7 + 2323644416*x**6 + 2638741504*x**5 + 411828224*x**4 + 1716256768*x**3 + 153223688*x**2 + 2411070754*x + 2359493543
# Decryption via cycling:
pt = ct
for _ in range(2**1025 - 3):
  pt = pt**e % n
# Assert decryption didn't work:
assert ct != pow(pt, e, n)

# Print flag:
print(pt)
