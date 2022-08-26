key = bytes.fromhex('10a58869d74be5a374cf867cfb473859')
pt = bytes.fromhex('00000000000000000000000000000000')

# key expansion
rc = [0x80, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
expanded = key
for i in range(4, 44):
    if i % 4 == 0:
        expanded.append(expanded[-4] ^ sub(rot(expanded[-1])) ^ (rc[i // 4] << 24))