import numpy as np
import galois

GF = galois.GF(2)

n = 100
while True:
    mat = GF.Random((n, n))
    if np.linalg.matrix_rank(mat) == n:
        break

state = GF.Random((n,))
rhs = mat @ state
print(mat)
print(state)
print(rhs)

_state = np.linalg.solve(mat, rhs)
print(_state)