from secret import priv

zeros = 0


def diff_add(P, Q, D):
    if Q == (1, 0):
        global zeros
        zeros += 1

    (x1, z1), (x2, z2), (x3, z3) = P, Q, D
    x_add = z3 * (x1 * x2 - z1 * z2) ^ 2
    z_add = x3 * (x1 * z2 - z1 * x2) ^ 2
    x_mul = (x1 ^ 2 - z1 ^ 2) ^ 2
    z_mul = 4 * x1 * z1 * (x1 ^ 2 + a * x1 * z1 + z1 ^ 2)
    return (x_add, z_add), (x_mul, z_mul)


def add_mul(P, Q, R, k):
    A, B, C = Q, Q, P
    C, B = diff_add(B, C, R)

    for d in reversed(ZZ(k).digits(2)[:-1]):
        if d == 0:
            B, _ = diff_add(A, B, Q)
            C, A = diff_add(A, C, P)
        else:
            A, _ = diff_add(B, A, Q)
            C, B = diff_add(B, C, R)

    return C


def test_add_mul(k):
    # assumes R = Q - P
    # returns P + [k]Q
    P, Q = var('P'), var('Q')
    R = Q - P
    A, B, C = 0, Q, P

    def tmp(P, Q, D):
        assert (P - Q - D) * (Q - P - D) == 0
        print(f'[{k}] add({P}, {Q})')
        return P + Q, 2 * P

    A, _ = tmp(B, A, Q)
    C, B = tmp(B, C, R)

    for d in reversed(ZZ(k).digits(2)[:-1]):
        if d == 0:
            # A, B, C -> 2A, A + B, A + C
            B, _ = tmp(A, B, Q)
            C, A = tmp(A, C, P)
        else:
            # A, B, C -> A + B, 2B, B + C
            A, _ = tmp(B, A, Q)
            C, B = tmp(B, C, R)

    return C


def point_to_xz(P):
    return (P[0], 1)


def xz_to_point(P):
    return E0.lift_x(P[0] / P[1])


lA, eA = 2, 91
lB, eB = 3, 57
p = lA ^ eA * lB ^ eB - 1

F = GF(p ^ 2, modulus=x ^ 2 + 1, name='z')
z = F.gen(0)

a, b = 6, 1
E0 = EllipticCurve(F, [0, a, 0, b, 0])
E0.set_order((p + 1) ^ 2, num_checks=0)


def test_optimization(P, Q):
    D = Q - P
    P, Q, D = map(point_to_xz, [P, Q, D])
    K = xz_to_point(add_mul(P, Q, D, priv))
    print(f"Optimization saved us {zeros} calculations!")

def main():
    print("Thank you for using grhkm's calculation service!")
    print("We are testing a beta feature - ")
    # test_add_mul(priv)
    PA, QA = (lB ^ eB * G for G in E0.gens())
    print("Testing Alice...")
    test_optimization(PA, QA)

    PB, QB = (lA ^ eB * G for G in E0.gens())
    print("Testing Bob...")
    test_optimization(PB, QB)

    print("You can test it as well! Just specify the x coordinate of P and Q")
    for _ in range(eA):
        