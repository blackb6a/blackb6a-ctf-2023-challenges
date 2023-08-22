# Loads `d`, a multivariate polynomial :yayy:
R.<a, b, c> = QQ[]

load("secret.sage")
assert d.parent() is R

# Removing constant term >3<
red_d = d - d[(0, 0, 0)]
assert len(list(d)) == 6 and max(map(abs, red_d.coefficients())) <= 30

# Sample invertible matrix from ZZ^{3x3}, with reasonable coefficients
# Goussian sampling from an unpublished manuscript
def sample_from_SL_ZZ(n):
    # WTF grhkm really said "there's a problem" then buff the challenge :wtf:
    w, x, y, z = [randint(-2**8, 2**8) for _ in range(4)]
    L = Matrix(ZZ, [[1, 0, 0], [w, 1, 0], [w**3 + 5 * w * x + x**2, x, 1]])
    U = Matrix(ZZ, [[1, 0, 0], [y, 1, 0], [y**3 + 5 * y * z + z**2, z, 1]])
    return 1 / (L * U.T)

# Obfuscate matrix
T = sample_from_SL_ZZ(3)
M = block_matrix(QQ, [[T, random_matrix(Zmod(2**16), 3, 1)], [0, Matrix([[1]])]])

_a, _b, _c, _d = M * vector([a, b, c, 1])
assert _d == 1
d = d.subs(a=_a, b=_b, c=_c)

open("trapdoor.sage", "w").write("M = Matrix(QQ, 4, 4, {})".format(M.list()) + "\n")
open("equation.py", "w").write("d = lambda a, b, c: {}".format(str(d).replace("^", "**")) + "\n")
print("Generated trapdoor!")
