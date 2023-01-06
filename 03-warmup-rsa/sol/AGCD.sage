def find_roots(a, k, N, beta, mu, mask_bit, m=40):
    """
    Given
    - f(x) := x + a
    - k, N where k = N^mu
    - exists p | N, where p >= N^beta
    
    Then we can find all x_0 such that
    - f(x_0) = 0 mod kp
    - |x_0| <= N^(beta^2 + mu)
    """

    X = 2^mask_bit

    print(f"[2] Find all roots with |x0| <= {X}")

    t = int(beta * m)
    db = log(k * X) * ((m^2 + m) / 2) + ((t^2 + t) / 2) * log(N)
    ub = (m + 1) * (m * log(k) + (beta * t) * log(N))
    assert db <= ub, f'db > ub since e^{db.n()} > e^{ub.n()}'

    _.<x> = QQ[]
    f = x + a
    
    mat = Matrix(ZZ, m + 1)
    for i in range(m + 1):
        _f = f(x = x * X)^i * k^(m - i) * N^(max(0, t - i))
        for j, cf in enumerate(_f.coefficients(sparse=False)):
            mat[i, j] = cf

    print(f"[2] Starting LLL of {m + 1} x {m + 1} matrix")
    mat = mat.LLL()

    _.<t> = QQ[]

    polys = []
    for i in range(m + 1):
        g = 0
        for j in range(m + 1):
            g += ZZ(mat[i, j] / X^j) * t^j
        polys.append(g)

        B = Ideal(polys).groebner_basis()
        for poly in B:
            if poly.degree() == 1:
                return -poly[0]