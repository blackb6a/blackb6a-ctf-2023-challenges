cmd_/home/bottom/blackb6a-ctf-2023-challenges/10-kernpass/src/kernel_driver/modules.order := {   echo /home/bottom/blackb6a-ctf-2023-challenges/10-kernpass/src/kernel_driver/kernpass.ko; :; } | awk '!x[$$0]++' - > /home/bottom/blackb6a-ctf-2023-challenges/10-kernpass/src/kernel_driver/modules.order