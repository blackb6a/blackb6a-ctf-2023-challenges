cmd_/home/bottom/blackb6a-ctf-2023-challenges/10-kernpass/src/kernel_driver/kernpass.mod := printf '%s\n'   kernpass.o | awk '!x[$$0]++ { print("/home/bottom/blackb6a-ctf-2023-challenges/10-kernpass/src/kernel_driver/"$$0) }' > /home/bottom/blackb6a-ctf-2023-challenges/10-kernpass/src/kernel_driver/kernpass.mod
