import glob
import galois
import numpy as np
from tqdm import tqdm, trange
from rev_mt import MT19937_64

EMPTY = set()
coef_mat = None
GF = galois.GF(2)


def add(v1, v2):
    return [x ^ y for x, y in zip(v1, v2)]


def int64_to_vec(x):
    return [(x >> i) & 1 for i in range(64)]


def _lshift_vec(vec, k):
    return [EMPTY] * k + list(vec)[:-k]


def _rshift_vec(vec, k):
    return list(vec)[k:] + [EMPTY] * k


def _mask_mask(vec, mask):
    _mask = int64_to_vec(mask)
    return [vec[i] if k else EMPTY for i, k in enumerate(_mask)]


def _mask_const(term, const):
    _mask = int64_to_vec(const)
    return [term if k else EMPTY for k in _mask]


def _process_vec(y):
    y = add(y, _mask_mask(_rshift_vec(y, 29), 0x5555555555555555))
    y = add(y, _mask_mask(_lshift_vec(y, 17), 0x71d67fffeda60000))
    y = add(y, _mask_mask(_lshift_vec(y, 37), 0xfff7eee000000000))
    y = add(y, _rshift_vec(y, 43))
    return y


const = 0xb5026f5aa96619e9


def twist():
    global state
    print("[+] twist()", flush=True)
    for i in range(312):
        # print("[*]", state[i], state[(i + 1) % 312], flush=True)
        # y = _mask_mask(state[(i + 1) % 312], lower) + _mask_mask(state[i], upper)
        state[i] = state[(i + 1) % 312][1:31] + state[i][31:] + [EMPTY]
        state[i] = add(state[i], state[(i + 156) % 312])
        state[i] = add(state[i], _mask_const(state[(i + 1) % 312][0], const))


def main():
    global state, coef_mat

    print("Loading data", flush=True)
    with open("public/output_69.txt", "r") as fin:
        ct = bytes.fromhex(fin.readline().split(" = ")[1].strip())
        iv = bytes.fromhex(fin.readline().split(" = ")[1].strip())
        iv = int.from_bytes(iv, "big")

    bits = [None] * 64 + list(map(int, bin(iv)[2:].zfill(20000 - 64)[::-1]))
    print("bits:", bits[:100], flush=True)

    print("Initialising variables", flush=True)
    state = [[{i * 64 + j} for j in range(64)] for i in range(312)]

    # load test seed
    print("Loading test seed")
    correct_state = MT19937_64(seed=69).mt
    correct_coef = []
    for i in range(len(correct_state)):
        for j in range(64):
            correct_coef.append((correct_state[i] >> j) & 1)
    correct_coef = np.array(correct_coef, dtype=bool)

    coef_mat = []
    rhs = bits[64:]

    # load coefficients
    if 'dump2' in glob.glob('*'):
        print("Loading coefficients from dump2", flush=True)
        coef_mat = np.loadtxt(open('dump2', 'r'))
        coef_mat = GF(np.array(coef_mat, dtype=int))

    else:
        print("Calculating coefficients", flush=True)
        idx = 0
        for i in range(len(bits)):
            # for i in range(1000):
            if idx == 0:
                twist()

            y = state[idx]
            idx = (idx + 1) % 312
            if bits[i] is None:
                continue

            y = _process_vec(y)
            msb = y[63]

            calculated = sum(correct_coef[k] for k in msb) % 2
            # print(f"[{i:<5}]", calculated, "==", bits[i], flush=True)
            assert calculated == bits[i]

            if idx == 0:
                print(f"[{i:<5}]", msb, "==", bits[i], flush=True)

            # extract coefficients from msb
            row = np.array([0] * (312 * 64), dtype=bool)
            for k in msb:
                row[k] = 1
            coef_mat.append(row)

        coef_mat = np.array(coef_mat, dtype=bool)

    print("TESTING")
    correct_recover = ''.join(map(str, rhs[64:300]))
    our_recover = ''.join(
        map(str,
            np.matmul(coef_mat, correct_coef, dtype=bool)[64:300]))
    print("Correct:", correct_recover)
    print(" We got:", our_recover)
    assert correct_recover == our_recover

    # dump coefficients
    print("Started dumping coefficients...", flush=True)
    with open('dump', 'w') as fout:
        for line in tqdm(coef_mat):
            fout.write(' '.join(map(lambda t: str(int(t)), line)) + '\n')

    print("Started solving equations...", flush=True)
    print("[numpy] BYE")

    # res = coef_mat.solve_right(rhs)
    # print("solution:", res, flush=True)

    # ker = coef_mat.right_kernel()
    # print("kernel:", ker, flush=True)

    # for ker in coef_mat.right_kernel():
    #     print(res + ker, flush=True)

    # state = [vec_to_int64(x) for x in state]
    # assert _process_vec(state[0]) == int64_to_vec(10331993320712037408), f"{_process(state[0])} != 10331993320712037408"


if __name__ == "__main__":
    main()