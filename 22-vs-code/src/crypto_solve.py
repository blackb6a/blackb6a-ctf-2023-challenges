from itertools import pairwise, zip_longest
from math import floor
from sage.all import vector, RR
from PIL import Image

intensities = '0000511D6300CF609C709645A78432005642574171487021003C451900274D35D762755E8B629C5BA856AF57BA649530C167D1512A272A3F6038604460398526BCA2A968DB6F8957C768BE5FBE2FB467CF5D8D5B795DC7625B5DFF50DE64C466DB2FC47CD860A65E9A2EB96CB54CE06DA763AB2EA26860524D3763536601005116008177A8705E53AB738E6A982F88BAA35B5F5B626D9C636B449B737E5B7B678598869A662F6B5B8542706C704C80736A607578685B70594A49715A4522'

pixels = [floor(int(intensities[i:i+2], base=16)*4/5) for i in range(0,len(intensities),2)]

pairs = [vector(pixels[i:i+2]) for i in range(0,len(pixels),2)]


with Image.open("./chall.png") as im:
    rgb_im = im.convert('RGB')
    bg = vector(rgb_im.getpixel((rgb_im.width-1,0)))

    pair_pools = []
    # pixel_pools = []
    for i in range(-bg[0],256-bg[0]):
        pair_pools.append(set(tuple(round(x) for x in l*i/255) for l in pairs))
        # pixel_pools.append(set(round(l*i/255) for l in pixels))

    # # verify raw to image algorithm is correct
    # with Image.open("./blackb6a-ctf-2023-challenges/22-vs-code/src/_resources/correct_letters.png") as im:
    #     for i in range(len(pairs)):
    #         assert tuple(pairs[i]) == tuple(im.getpixel((i,j)) for j in range(2))

    #     print("Raw to image assertion complete\n")


    # # verify the color calculation algorithm is correct
    # color = vector((0xFF, 0xBE, 0x33))
    # for i,x in enumerate("import"):        
    #     for j,intensity in enumerate(pairs[ord(x)-0x20]):
    #         assert tuple(round(x) for x in (color-bg)*intensity/255+bg) == rgb_im.getpixel((i,j))
    #     print(x, (rgb_im.getpixel((i,j)), rgb_im.getpixel((i,j+1))))

    # print("Color calculation algorithm assertion complete\n")

    # color = vector((0x8F, 0x4F, 0x56))
    def gen_reference(s, coord):
        return [[(coord[1]-1+i, coord[0]-1),c] for i,c in enumerate(s)]
    reference = []
    reference += gen_reference("flags", (11,53))

    # for coord, letter in reference:
    #     if letter == ' ':
    #         continue
    #     pair_info = [
    #         tuple(vector(rgb_im.getpixel((coord[0],coord[1]*2+i)))-bg) for i in range(2)
    #     ]
    #     channels = tuple(zip(*pair_info))
    #     for ch, cl in zip(channels, color):
    #         assert all(x in pixel_pools[cl] for x in ch)
    #         assert ch in pair_pools[cl]
    # print("Actual image color works")

    candidates = [list(range(256)) for _ in range(3)]
    for coord, letter in reference:
        pair_info = [
            tuple(vector(rgb_im.getpixel((coord[0],coord[1]*2+i)))-bg) for i in range(2)
        ]
        channels = tuple(zip(*pair_info))
        for i, ch in enumerate(channels):
            candidates[i] = [x for x in candidates[i] if ch in pair_pools[x]]
            if len(candidates[i]) == 0:
                print(f"Channel #{i} failed")
        print(letter, *[[hex(x)[2:] for x in l] if len(l)>1 else hex(l[0])[2:] for l in candidates])