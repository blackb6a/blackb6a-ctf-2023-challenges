FROM ubuntu:22.10

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        tini xinetd \
        qemu-system \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home kernpass && mkdir -p kernpass

COPY ./src /home/kernpass/
COPY ./app.xinetd /etc/xinetd.d/app

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

RUN chmod 555 /home/kernpass/run.sh

WORKDIR /home/kernpass
EXPOSE 9999

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]
