def elligator_attack(target):
    u, v = target.xy()
    try:
        r1 = ((-A / u - 1) / Z).square_root()
    except:
        r1 = None
    try:
        r2 = ((A / (u + A) - 1) / Z).square_root()
    except:
        r2 = None
    return (r1, r2)
