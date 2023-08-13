FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

RUN /home/ctfuser/venv/bin/pip uninstall crypto
RUN /home/ctfuser/venv/bin/pip uninstall pycryptodome
RUN /home/ctfuser/venv/bin/pip install pycryptodome galois

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
COPY start.sh /home/ctfuser/
RUN python3 -m compileall /home/ctfuser/

RUN chown -R root:root /home/ctfuser/ && \
    find /home/ctfuser/ -type d -exec chmod 555 {} \; && \
    find /home/ctfuser/ -type f -exec chmod 444 {} \;

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /bin/bash /home/ctfuser/start.sh"
