# The idea is that for an elliptic curve y^2 = x^3 + ax^2 + bx + c,
# the discriminant equals Delta = -a^2(ac - b^2) / 4 - b^3 / 64 - 27c^2 / 256 + 9abc / 128,
# Delta = -256^-1 (64a^3c - 64a^2b^2 + 4b^3 + 27c^3 - 18abc)
# To find a curve with such discriminant, the intended solution is to then
# use the Modularity theorem, which states that every elliptic curve E with
# conductor Cond(E) has an associated *newform* of weight 2 and level Cond(E),
# where the prime factors of d and Cond(E) are equal. Therefore, we can just
# compute the newforms of weight 2 and level d, then compute their elliptic
# curve models (if exists) and check whether the discriminant is as desired.

# Implement!
import sys

nfs = [u for u in Newforms(307, 2, names="t") if u.base_ring() == QQ]
E = nfs[2].abelian_variety().elliptic_curve().short_weierstrass_model()
# Backup: E = EllipticCurve(QQ, [16, -48])
print(E)
print(E.discriminant())

# Load trapdoor
load("trapdoor.sage")
assert "M" in globals()
Minv = M^-1

# Load equation
from equation import d
assert "d" in globals()

# Initiate connection
from pwn import context, process
context.log_level = "CRITICAL"
rc = process("python3 chal.py", shell=True)

# Load equation
# TODO: Generate trapdoor dynamically and adjust script
# For now, it is a nop
rc.recvuntil(b"Equation: ")
rc.recvline()

cnt = 0
while cnt < 1000:
    if cnt % 50 == 49:
        print(f"Progress: {cnt + 1} / 1000")
    Et = E.change_weierstrass_model([1, randrange(2^2048), 0, 0])
    r0, a, r1, b, c = Et.a_invariants()
    if r0 != 0 or r1 != 0:
        continue
    # print(a, b, c)
    # print(Et, Et.discriminant())
    a, b, c, _ = Minv * vector([a, b, c, 1])
    print(a, b, c, file=sys.stderr)
    assert d(a, b, c) == 0
    rc.sendlineafter(b": ", str(a).encode())
    rc.sendlineafter(b": ", str(b).encode())
    rc.sendlineafter(b": ", str(c).encode())
    cnt += 1

print(rc.recvline().decode().strip())

