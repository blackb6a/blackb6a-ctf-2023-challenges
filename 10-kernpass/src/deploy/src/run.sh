#!/bin/sh
qemu-system-x86_64 \
    -m 2048M \
    -nographic \
    -kernel bzImage \
    -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
    -no-reboot \
    -cpu kvm64,+smap,+smep \
    -monitor /dev/null \
    -initrd rootfs.cpio \
    -netdev user,id=net \
        -device e1000,netdev=net \
	    -net nic,model=virtio \
	        -net user 
