n = 140929132326515701830061537809640902585185813416109793390760091768710390508438129373664386804267405755660755924391168069848181903970721313280237136505746584393209134554048315944592420200755976487390774661241246083529120014508030767016350179906797779729393468376144702411661608064480979315640326582762998663731
e = 33009148670824201015693841
lp = 255361231373666385833957541849572037145396072690525140044755
lq = 7966667333790279090405974163791191286346981658686366523146573

c = 98596145982109216173214971454142511539176647522355961021171564738116930501067321033236962430859641261401926175024157254415469218392316947611023810984395560766357118910981397983100107255364976808942660149202144743970189683031221230349236868694349173854003572677362663288993577685874924096100398730784674303569

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
f = f.change_ring(R)

# Took 165 seconds to finish on my machine
first_roots = small_roots(f, bounds, m=4, d=5)

for kp, kq in first_roots:
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