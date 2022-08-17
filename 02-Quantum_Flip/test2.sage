n = int(input("n: "))
mat = random_matrix(GF(2), n, n)
mat_str = str(mat).replace('[', '').replace(']', '')
with open('dump2', 'w') as fout:
    fout.write(mat_str)
