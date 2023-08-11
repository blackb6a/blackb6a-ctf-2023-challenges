n = 96446191626393604009054111437713980755082681332020571709789032122186639773874753631630024642568257679734714430483780317122960230235124140242511126339536047435591010087751700582288534654352742251068909342986464462021206713195415006300821397979265537607226612724482984235104418995222711966835565604156795231519
e = 21859725745573183363159471
lp = 5170537512721293911585823686902506016823042591640808668431139
lq = 2408746727412251844978232811750068549680507130361329347219033
c = 22853109242583772933543238072263595310890230858387007784810842667331395014960179858797539466440641309211418058958036988227478000761691182791858340813236991362094115499207490244816520864518250964829219489326391061014660200164748055767774506872271950966288147838511905213624426774660425957155313284952800718636

# e*dp = 1 + kp*(p-1), where dp = lp + 2^204*up
#
# Rearranging, we have
# 
#   e*dp + kp-1 = kp*p
#
# Multiplying with the another, we have
#
#   (e*dp + kp-1) * (e*dq + kp-1) = kp*kq*p*q = kp*kq*n
#
# Taking mod e*2^204, we have
#
#   (e*lp + kp-1) * (e*lq - kp-1) = kp*kq*n
#
# The above congruence has unknowns kp and kq. Find them with LLL.
# By the way, all coefficients are even numbers. Simply divide the mod and the coefficients by 2.

load('coppersmith.sage')

bounds = (2^85, 2^85)

R = Zmod(e * 2^203)
P.<kp, kq> = PolynomialRing(ZZ)

f = (e*lp + kp-1) * (e*lq + kq-1) - kp*kq*n
f /= 2
print(f'{f = }')
f = f.change_ring(R)

# Took 165 seconds to finish on my machine
first_roots = small_roots(f, bounds, m=4, d=5)

for kp, kq in first_roots:
    print(f'{kp, kq = }')
    # tp = p mod e*2^203, tq = q mod e*2^203
    tp = int((lp * e - 1 + kp) * pow(kp, -1, e*2^203))
    tq = int((lq * e - 1 + kq) * pow(kq, -1, e*2^203))
    
    bounds = (2^244, 2^244)

    R = Zmod(n)
    P.<sp, sq> = PolynomialRing(R)

    f = (e*2^203*sp + tp)*(e*2^203*sq + tq) - n

    # Took 15 seconds to finish
    second_roots = small_roots(f, bounds, m=4, d=6)

    for sp, sq in second_roots:
        p = int(e*2^203*sp + tp)
        q = int(e*2^203*sq + tq)
        if p*q != n: continue

        phi_n = (p-1)*(q-1)
        d = int(pow(e, -1, phi_n))

        m = pow(c, d, n)
        m = int(m).to_bytes(1024//8, 'big')
        print(f'{m = }')