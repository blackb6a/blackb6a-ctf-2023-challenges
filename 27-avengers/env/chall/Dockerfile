FROM sagemath/sagemath:10.0

RUN useradd ctfuser --create-home

RUN sudo apt-get update

RUN sudo apt-get install -y socat

COPY *.sage /home/sage/

ENV FLAG "b6actf{i_dont_like_leet_stuff_so_ye_hope_u_enjoyed_the_comments}"

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'sage /home/sage/prover.sage'"]
