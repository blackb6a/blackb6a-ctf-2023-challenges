import galois
import numpy as np
import base64

from OV import OilVinegar
from FruitHill import Fruit

from secret import WATER_TAP, flag

def getPepperOrSalt(q, v):
    return galois.GF(q).Random(v // 2)

def getSause(q, n):
    secret_sause = galois.GF(q).Random((n, n))
    while np.linalg.matrix_rank(secret_sause) < n:
        secret_sause = galois.GF(q).Random((n, n))
    return secret_sause

def vecToBase64(vec):
    vec = np.reshape(vec, (-1, 8))
    bin2Byte = 1 << np.arange(8, dtype=np.ubyte)[::-1]
    return base64.b64encode(bytes(vec @ bin2Byte))

def encodeRecipe2Pub(recipe2):
    return b':'.join([vecToBase64(pub.view(np.ndarray)) for pub in recipe2.pub])

def printRecipesPub(recipe1, recipe2):
    print("=========================================================================")
    print(f"Recipe 1: Sorry this recipe is highly secret so I cannot give you any info about it!")
    print(f"Recipe 2: {encodeRecipe2Pub(recipe2).decode()}")
    print("=========================================================================")

def main():
    
    q = 2
    o = 64
    v = 64
    n = o + v

    assert len(WATER_TAP) == (v // 2) # WATER_TAP is ont-hot encoding of the water tabs
    salt = getPepperOrSalt(q, v)
    pepper = getPepperOrSalt(q, v)
    secret_sause = getSause(q, n)
    
    recipe1 = Fruit(q, n, secret_sause)
    recipe2 = OilVinegar(q, o, v, WATER_TAP, salt, pepper, secret_sause)

    printRecipesPub(recipe1, recipe2)
    print("Please give me the following two dishes!")
    print("1. Cooked with recipe 1 using the MSG 'cryptochefisgood'")
    print("2. Cooked with recipe 2 using the MSG 'ilovemsg'")
    print("Of course, you can cook a few dishes with me to get some cooking skills first.")

    for _ in range(32):
        cmd = input("> ")
        args = cmd.split(' ')
        if args[0] == 'cook':
            rec, msg = int(args[1]), args[2]

            if rec != 1 and rec != 2:
                raise Exception("Invalid recipe!")
            recipe = recipe1 if rec == 1 else recipe2

            msg = base64.b64decode(msg.encode())
            if msg == b'cryptochefisgood' or msg == b'ilovemsg':
                raise Exception("Sorry, but you have to learn the dishes yourself!")
            
            msg = list(map(int, ''.join(format(b, '08b') for b in msg)))
            print(f"Cooked dish: {vecToBase64(recipe.cook(msg).view(np.ndarray)).decode()}")
        
        elif args[0] == 'check':
            rec, sig, msg = int(args[1]), args[2], args[3]

            if rec != 1 and rec != 2:
                raise Exception("Invalid recipe!")
            recipe = recipe1 if rec == 1 else recipe2

            sig = base64.b64decode(sig.encode())
            msg = base64.b64decode(msg.encode())

            sig = list(map(int, ''.join(format(b, '08b') for b in sig)))
            msg = list(map(int, ''.join(format(b, '08b') for b in msg)))

            if recipe.verify(sig, msg):
                print("Yes! This dish is made from that msg.")
            else:
                print("Hum... Seems a bit off.")
        
        elif args[0] == 'skip':
            break
        
    print("=========================================================================")
    print("It's time for the final test!")

    print("Please give me dish with recipe 1 using the MSG 'cryptochefisgood':")
    sig = input('> ')

    sig = base64.b64decode(sig.encode())
    msg = b'cryptochefisgood'

    sig = list(map(int, ''.join(format(b, '08b') for b in sig)))
    msg = list(map(int, ''.join(format(b, '08b') for b in msg)))

    if recipe1.verify(sig, msg):
        print("Nice! You have mastered this recipe!")
    else:
        print("Hum... Please come again after you have sharpened your cooking skills.")
        exit(0)
    
    print("=========================================================================")
    print("Please give me dish with recipe 2 using the MSG 'ilovemsg':")
    sig = input('> ')

    sig = base64.b64decode(sig.encode())
    msg = b'ilovemsg'

    sig = list(map(int, ''.join(format(b, '08b') for b in sig)))
    msg = list(map(int, ''.join(format(b, '08b') for b in msg)))

    if recipe2.verify(sig, msg):
        print("Congratulations! You have mastered all the recipes!")
    else:
        print("Hum... Please come again after you have sharpened your cooking skills.")
        exit(0)
    
    print(f"Here's your reward: {flag}")


if __name__ == '__main__':
    main()