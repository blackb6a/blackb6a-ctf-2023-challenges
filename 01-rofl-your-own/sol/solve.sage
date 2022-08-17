from pwn import *
from colorama import Fore, Style


def generate_pf():
    np = list(prime_range(4096, 16384))
    cand = []
    while True:
        tmp = set()
        prod = 1  # 2q - 1
        while prod.nbits() < 513:
            c = choice(np)
            if c not in tmp:
                tmp.add(c)
                prod *= c

        if prod.nbits() != 513:
            continue

        q = (prod + 1) // 2
        if is_prime(4 * q - 1):
            return q, sorted(list(tmp))


def dlog(g, a):
    k, r = 1, g
    while r != a:
        r *= g
        k += 1
    return k


def main():
    q, pf = generate_pf()
    print("pf:", pf)

    assert product(pf) == 2 * q - 1
    # p = -4 * q + 1
    p = 4 * q - 1

    r = process('python3 ../src/chall.py', shell=True)
    for _ in range(256):
        print(f"Challenge {_ + 1}!")

        try:
            r.recvuntil(b'q = ')
        except EOFError:
            print('[EOFError] Failed...')
            r.close()
            return

        r.sendline(str(-q).encode())

        r.recvuntilb('g = ')
        g = ZZ(r.recvline())

        r.recvuntil(b'h = ')
        h = ZZ(r.recvline())

        g, h = GF(p)(g), GF(p)(h)

        # g^x == h mod p
        rem, mods = [], []
        phi = p - 1
        for _p in [2] + pf:
            _g = g ^ (phi // _p)
            _h = h ^ (phi // _p)
            _d = dlog(_g, _h)
            _ord = dlog(_g, 1)

            if _ord != _p:
                print(f"[!] Reduced order: {_p} -> {_ord}")
            rem.append(_d)
            mods.append(_ord)

        _sol = CRT(rem, mods)
        _mod = LCM(mods)

        sols = 1 + (2 ^ 512 - _sol) // _mod
        if sols > 1:
            print('[Oh no!] Number of sols in [0, 2^512):', sols)

        r.recvuntil(b'x = ')
        r.sendline(str(_sol).encode())

    r.recvuntil(b'[*] ')
    flag = r.recvline().strip().decode()
    print(f'{Fore.CYAN}Flag: {flag}{Style.RESET_ALL}')
    exit(0)


if __name__ == '__main__':
    while True:
        main()