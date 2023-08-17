load("ehasher.sage")
load("chasher.sage")
assert "EHasher" in globals()
assert "CHasher" in globals()

class Protocol:
    def __init__(self):
        self.ehasher = EHasher()
        self.chasher = CHasher()

    def sign(self, msg):
        h = self.ehasher.hash(msg)
        c = self.chasher.hash(h)
