from pwn import *

r = remote("chall.pwnable.hk", 20003)
#r = remote("127.0.0.1", 1337)
with open("solve", 'rb') as file:
    data = file.read()

file_size = len(data)
print(f"file size: {file_size}")
r.sendline(str(file_size))
sleep(1)
print("Upload data")
r.send(data)
sleep(10)
