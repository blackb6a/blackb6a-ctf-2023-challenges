# Found a fruit hill!
# Let's use the fruits here too!

import galois # galois is used just because it's more lightweighted when compared to sage 
import numpy as np

class Fruit:

    def __init__(self, q, n, secret_sause):
        
        self.n = n
        self.GF = galois.GF(q)
        self.SS = self.GF(secret_sause)

    # Do you know what is msg? msg makes everything good. If your dish is not delicious, add msg.
    # If your life is not good, add msg, it will be a lot better.
    def cook(self, msg):
        assert len(msg) == self.n
        msg = self.GF(msg)
        tastyDish = self.SS @ msg
        return tastyDish
    
    # Verify whether you really add the msg in that tasty dish!
    def verify(self, tastyDish, msg):
        tastyDish = self.GF(tastyDish)
        msg = self.GF(msg)
        taste = np.linalg.inv(self.SS) @ tastyDish
        return np.all(taste == msg)
        