def test_add_mul(k):
    # assumes R = Q - P
    # returns P + [k]Q
    P, Q = var('P'), var('Q')
    R = Q - P

    def tmp(P, Q, D):
        assert (P - Q - D) * (Q - P - D) == 0
        print(f'[{k}] add({P}, {Q})')
        return P + Q, 2 * P

    A, B, C = Q, Q, P
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


if __name__ == '__main__':
    k = int(input("k: "))
    test_add_mul(k)