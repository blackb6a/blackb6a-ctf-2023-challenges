from itertools import chain
from math import floor
from sage.all import vector, RR
from PIL import Image

intensities = '0000511D6300CF609C709645A78432005642574171487021003C451900274D35D762755E8B629C5BA856AF57BA649530C167D1512A272A3F6038604460398526BCA2A968DB6F8957C768BE5FBE2FB467CF5D8D5B795DC7625B5DFF50DE64C466DB2FC47CD860A65E9A2EB96CB54CE06DA763AB2EA26860524D3763536601005116008177A8705E53AB738E6A982F88BAA35B5F5B626D9C636B449B737E5B7B678598869A662F6B5B8542706C704C80736A607578685B70594A49715A4522'

pixels = [floor(int(intensities[i:i+2], base=16)*4/5) for i in range(0,len(intensities),2)]

pairs = [vector(pixels[i:i+2]) for i in range(0,len(pixels),2)]

def gen_reference(s, coord):
    return [((coord[1]-1+i, coord[0]-1),c) for i,c in enumerate(s)]

with Image.open("../public/chall.png") as im:
    rgb_im = im.convert('RGB')
    bg = vector(rgb_im.getpixel((rgb_im.width-1,0)))

    def calculate(*references):
        reference = list(chain(*chain(gen_reference(*r) for r in references)))

        candidates = [list(range(256)) for _ in range(3)]
        for coord, letter in reference:
            pair_info = [
                tuple(vector(rgb_im.getpixel((coord[0],coord[1]*2+i)))-bg) for i in range(2)
            ]
            channels = tuple(zip(*pair_info))
            for i, ch in enumerate(channels):
                temp = [x for x in candidates[i] if tuple(round(x) for x in pairs[ord(letter)-32]*(x-bg[0])/255) == ch]
                # if len(temp) != len(candidates[i]):
                #     print(letter, pairs[ord(letter)-32])
                candidates[i] = temp
                if len(candidates[i]) == 0:
                    print(f"Channel #{i} failed")
            
            if all(len(x)==1 for x in candidates):
                print(letter, *[hex(l[0])[2:] for l in candidates])
                break
        else:
            print(letter, *[[hex(x)[2:] for x in l] for l in candidates])
    
    calculate(("#!/u", (1,1)))
    calculate(("__import__", (11,12)))
    calculate(('def', (10,1)))
    calculate(
        ('72', (48,18)),
        ('0', (54,16))
    )
    calculate(('W', (26,43)))
    calculate(('des', (53,5)))
    calculate(('type', (18,32)))
    calculate(("jso", (2,8)))
    calculate(("impor", (2,1)))
    calculate(
        ('*', (40,5)),
    )
    calculate(
        ('is', (18,43)),
        ('not', (36,12)),
    )
    calculate(
        ('Fa', (18,94))
    )
    calculate(("\\x6", (8,20)))
    calculate(("A-Za-z", (8,40)))
    calculate(
        ("[", (8,39)),
        ("]+", (8,51)),
    )
    calculate(
        ('%F', (23,12))
    )