import sys
from Crypto.Util.number import bytes_to_long

from secret import flag

LOGGER = open('/dev/null', 'w')

lA, eA = 2, 216
lB, eB = 3, 137
p = lA ^ eA * lB ^ eB - 1

F = GF(p ^ 2, modulus=x ^ 2 + 1, name='z')
z = F.gen(0)

E0 = EllipticCurve(F, [0, 6, 0, 1, 0])

aP, aQ = [(lB ^ eB * G).xy() for G in E0.gens()]
bP, bQ = [(lA ^ eA * G).xy() for G in E0.gens()]

priv = bytes_to_long(flag)
assert priv < lA ^ eA and priv < lB ^ eB


def diff_add(P, Q, D):
    # https://hyperelliptic.org/EFD/g1p/data/montgom/xz/ladder/ladd-1987-m
    # Montgomery differential point additions

    # assumption: D = P - Q
    # returns: (P + Q, 2P)

    (x2, z2), (x3, z3), (x1, z1) = P, Q, D
    
    x_add = z3 * (x1 * x2 - z1 * z2) ^ 2
    z_add = x3 * (x1 * z2 - z1 * x2) ^ 2
    x_mul = (x1 ^ 2 - z1 ^ 2) ^ 2
    z_mul = 4 * x1 * z1 * (x1 ^ 2 + 6 * x1 * z1 + z1 ^ 2)

    return (x_add, z_add), (x_mul, z_mul)


def diff_add_mul(P, Q, D, k):
    # https://link.springer.com/chapter/10.1007/978-3-319-72565-9_4, Section 3.3
    # Three-point montgomery differential ladder

    # assumption: D = P - Q
    # returns: P + [k]Q

    A, B, C = Q, Q, P
    C, B = diff_add(B, C, D)

    for d in reversed(ZZ(k).digits(2)[:-1]):
        if d == 0:
            B, _ = diff_add(A, B, Q)
            C, A = diff_add(A, C, P)
        else:
            A, _ = diff_add(B, A, Q)
            C, B = diff_add(B, C, D)

    return C


def point_to_xz(P):
    return (P[0], 1)


def xz_to_point(P):
    return E0.lift_x(P[0] / P[1])


def test_optimization(P, Q, k=None):
    if k is None:
        k = priv

    correct = double_add_mul(P, Q, k)
    D = add(P, negation(Q))

    P, Q, D = map(point_to_xz, [P, Q, D])
    K = xz_to_point(diff_add_mul(P, Q, D, k))
    if correct[0] == K[0]:
        print("✅")
    else:
        print("❌")

    print(correct, K, file=LOGGER)


def main():
    print("Thank you for using grhkm's calculation service!")
    print("We offer the service to calculate P + [k]Q for your SIDH protocol.")
    print("We use the montgomery curves By^2 = x^3 + 6x^2 + x.")
    print("For example:")

    print("Testing Alice")
    test_optimization(aP, aQ, k=None)

    print("Testing Bob")
    test_optimization(bP, bQ, k=None)

    print(
        "You can test it as well! Just enter P = (Px, Py), Q = (Qx, Qy) and k")
    for _ in range(eA):
        Px = F(input("Px: "))
        Py = F(input("Py: "))
        Qx = F(input("Qx: "))
        Qy = F(input("Qy: "))
        k = (lambda s: ZZ(s) if len(s) else None)(input(" k: "))

        P = (Px, Py)
        Q = (Qx, Qy)
        test_optimization(P, Q, k=k)


if __name__ == '__main__':
    main()
