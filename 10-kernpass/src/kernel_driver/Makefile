obj-m = kernpass.o
KVERSION = $(shell uname -r)
all:
	make -C /lib/modules/5.19.0/build M=$(PWD) modules
	rm -rf *.o *.mod.* *.symvers *.order *.mod
	strip --strip-debug kernpass.ko
clean:
	make -C /lib/modules/$(KVERSION)/build M=$(PWD) clean; rm -rf *.o *.ko *.mod.* *.symvers *.order
