load("ehasher.sage")
load("chasher.sage")
assert "EHasherHellman" in globals()
assert "CHasherLorenz" in globals()
assert "CHasherPanny" in globals()

class Protocol:
    def __init__(self):
        self.ehasherorz = EHasherHellman
        self.ehashercat = EHasherRemy
        self.chashery = CHasherLorenz
        self.chasherx7 = CHasherPanny

    def yellman(self):
        return (self.ehasherorz, self.chashery)

    def remx7(self):
        return (self.ehashercat, self.chasherx7)

    def get_modulus(self, hasher):
        ehasher, chasher = hasher
        return 3**floor(log(chasher.p, 3) / 3)

    def hsign(self, hasher, msg):
        ehasher, chasher = hasher
        h = ehasher.hash(msg % ehasher.p)
        c, d = chasher.action(0, ZZ(h % 2**chasher.n).digits(2, padto=chasher.n))
        return c, d % self.get_modulus(hasher)

    def sign(self, msg):
        sig = []
        for hasher in self.hashers():
            sig.append(self.hsign(hasher, msg))
        return tuple(sig)

    def verify(self, msg, sig):
        return self.sign(msg) == sig

    def challenge(self):
        msg = os.urandom(10)
        msg_r = int.from_bytes(msg, "big")
        sig = self.sign(msg_r)
        print(sig)

Server = Protocol()
