# BusyBox

`find . | cpio -o --format=newc > ../../rootfs.img`

# Solve Script

gcc -E exp.c -o pre_exp.c
musl-gcc --static pre_exp.c -o exp
strip exp
gzip exp
base64 exp.gz > exp.gz.b64
cd solve
cp ../exp .
python3 upload.py
