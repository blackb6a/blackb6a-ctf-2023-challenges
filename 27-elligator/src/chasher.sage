proof.all(False)

class CHasher:
    def __init__(self, l):
        self.l = l
        self.p = 4 * product(self.l) - 1
        assert is_prime(self.p)

        self.K = GF(self.p**2, modulus=x**2 + 1, names="i")
        self.i = self.K.gen(0)

    def montgomery_curve(self, A):
        return EllipticCurve(self.K, [0, A, 0, 1, 0])

    def montgomery_coefficient(self, E):
        Ew = E.change_ring(GF(self.p)).short_weierstrass_model()
        _, _, _, a, b = Ew.a_invariants()
        R, z = GF(self.p)["z"].objgen()
        r = (z**3 + a * z + b).roots(multiplicities=False)[0]
        s = sqrt(3 * r**2 + a)
        if not is_square(s):
            s = -s
        return GF(self.p)(3 * r / s)

    def action(self, pub, priv):
        assert len(priv) == len(self.l)
        E = self.montgomery_curve(pub)
        es = list(priv)

        while any(es):
            E.set_order((self.p + 1)**2)
            P = E.lift_x(ZZ(randrange(self.p)))
            s = [-1, 1][P[1] in GF(self.p)]
            k = prod(l for l, e in zip(self.l, es) if sign(e) == s)
            P *= (self.p + 1) // k

            for i, (l, e) in enumerate(zip(self.l, es)):
                if sign(e) != s:
                    continue

                Q = k // l * P
                if not Q:
                    continue
                Q.set_order(l)
                phi = E.isogeny(Q)

                E, P = phi.codomain(), phi(P)
                es[i] -= s
                k //= l

        return self.montgomery_coefficient(E)

CHasherLorenz = CHasher(list(prime_range(3, 375)) + [587])
CHasherPanny = CHasher(list(prime_range(7, 47)) + [67])
