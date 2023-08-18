FROM sagemath/sagemath:10.0

RUN sudo apt-get update

RUN sudo apt-get install -y socat

WORKDIR /home/ctfuser

COPY *.sage /home/ctfuser/

ENV FLAG b6actf{???}

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'sage chall.sage'"]
