FROM ubuntu:22.10

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        qemu-system-x86 socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home kernpass && mkdir -p kernpass

COPY ./src /home/kernpass/

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

RUN chmod 555 /home/kernpass/run.sh

WORKDIR /home/kernpass
EXPOSE 9999

ENTRYPOINT socat -dd TCP4-LISTEN:9999,fork,reuseaddr EXEC:"timeout 600 /home/kernpass/run.sh"
