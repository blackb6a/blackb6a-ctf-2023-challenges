FROM python:buster
RUN apt-get -qqy update && \
    apt-get -qqy --no-install-recommends install \
    qutebrowser xvfb && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install flask

COPY server.py /
RUN echo '#!/bin/sh\necho flag{flag2}' > /proof_random_uuid.sh
RUN chmod 555 /server.py /proof_*.sh

WORKDIR /usr/share/javascript/pdf
WORKDIR /tmp

COPY pdfjs-1.10.88-dist.zip .
RUN unzip pdfjs-1.10.88-dist.zip -d pdfjs && \
    mv /tmp/pdfjs/* /usr/share/javascript/pdf && \
    rm -rf /tmp/*

RUN useradd kyubey --create-home
USER kyubey

WORKDIR /tmp
ENV FLAG flag{flag1}
ENV G_SITEKEY You_should_fix_the_reCAPTCHA_by_yourself
ENV G_SECRET You_should_fix_the_reCAPTCHA_by_yourself
ENV DISPLAY :99
CMD ["sh","-c","Xvfb :99 -screen 0 640x400x8 -nolisten tcp & python3 /server.py"] 