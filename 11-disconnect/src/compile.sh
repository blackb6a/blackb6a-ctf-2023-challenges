gcc sandbox.c -o sandbox;
gcc exp/solve.c -o exp/solve -static -luring -Os -Wl,--gc-sections -fno-stack-protector -z execstack
strip exp/solve
gcc exp/solve_webhook.c -o exp/solve_webhook --static -luring -Os -Wl,--gc-sections -fno-stack-protector -z execstack
strip exp/solve_webhook
