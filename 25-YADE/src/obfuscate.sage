T = 307

# Original discriminant equation
R.<a, b, c> = QQ[]
d = 4 * a**3 * c - a**2 * b**2 + 4 * b**3 + 27 * c**2 - 18 * a * b * c - T * 2^8

# Obfuscate matrix
gens = SL(3, ZZ).as_matrix_group().gens()
T = Matrix(QQ, product([choice(gens) for _ in range(2^7)]))
M = block_matrix([[T, random_matrix(Zmod(256), 3, 1).change_ring(QQ)], [0, Matrix([[1]])]])

_a, _b, _c, _d = M * vector([a, b, c, 1])
assert _d == 1
d = d.subs(a=_a, b=_b, c=_c)

open("trapdoor.sage", "w").write("M = Matrix(QQ, 4, 4, {})".format(M.list()) + "\n")
open("equation.py", "w").write("d = lambda a, b, c: {}".format(str(d).replace("^", "**")) + "\n")
print("Generated trapdoor!")
