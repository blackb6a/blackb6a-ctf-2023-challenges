FROM ubuntu:focal-20211006

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        tini xinetd \
        python3.9 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home pyjail3 && mkdir -p /home/pyjail3

COPY ./chall /home/pyjail3/
COPY ./app.xinetd /etc/xinetd.d/app
COPY ./chall/flag.txt /

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

WORKDIR /home/pyjail3
EXPOSE 1337

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]