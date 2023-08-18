# Compile
Put your public IP and listening Port (default 58888) in exp/solve.c

Then run `./complie.sh`

To test,
listen on local machine (Make sure your IP and Port is accessible from external network)
```
python3 -m http.server 58888
```

# Run test script
```
cd exp
python3 upload.py; python3 upload_webhook.py
```
View the flag on local machine or traffic "/b6actf" in webhook (https://public.requestbin.com/r/en6fb8xm9qefw)
