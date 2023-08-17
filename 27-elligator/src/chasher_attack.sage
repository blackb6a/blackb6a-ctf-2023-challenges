load("chasher_data.sage")


def lorenz_collider(priv):
    # Given a private vector priv, outputs an equivalent vector
    # First, convert it to a power of generator g = <3, pi - 1>
    s = sum(val * priv[idx] for idx, (_, val)
            in enumerate(csidh_512_dlog_list)) % csidh_512_class_number

    # Next, interpret this as a CVP problem, or SVP via Kannan's embedding
    n = len(csidh_512_dlog_list)
    mat = Matrix(ZZ, n + 2, n + 2)
    for i, (_, val) in enumerate(csidh_512_dlog_list):
        mat[i, 0] = val
        mat[i, i + 1] = 1
    mat[n, 0] = -s
    mat[n, n + 1] = 1
    mat[n + 1, 0] = csidh_512_class_number

    # Now, rescale it for better output quality
    ws = [2**256] + [1] * n + [2**64]
    W = diagonal_matrix(ws)

    # apply LLL to find short vectors
    L = (mat * W).LLL() / W
    for row in L:
        if row[0] == 0 and abs(row[-1]) == 1:
            break

    sol = row[1:-1]
    assert sum(val * sol[idx] for idx, (_, val)
               in enumerate(csidh_512_dlog_list)) % csidh_512_class_number == s

    return sol
