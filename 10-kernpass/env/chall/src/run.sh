#!/bin/sh
qemu-system-x86_64 \
    -m 2048M \
    -nographic \
    -kernel /home/kernpass/bzImage \
    -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
    -no-reboot \
    -cpu kvm64,+smap,+smep \
    -monitor /dev/null \
    -initrd /home/kernpass/rootfs.cpio
