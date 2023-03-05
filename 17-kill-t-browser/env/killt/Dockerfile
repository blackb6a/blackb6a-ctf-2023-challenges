FROM python:buster
RUN apt-get -qqy update && \
    apt-get -qqy --no-install-recommends install \
    qutebrowser xvfb && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install flask

COPY server.py /
RUN echo '#!/bin/sh\necho flag{Did_you_craft_a_0-Click-RCE_payload__or_just_d1rectory-l1sting-N-l0cal-f1le-r3ad}' > /proof_d2e4f0a6-55e8-4897-9ce0-e829cdc8279e.sh
RUN chmod 555 /server.py /proof_*.sh

WORKDIR /usr/share/javascript/pdf
WORKDIR /tmp
# RUN wget https://github.com/ppcrab/CVE-2018-5158/raw/main/pdfjs-1.10.88-dist.zip
COPY pdfjs-1.10.88-dist.zip .
RUN unzip pdfjs-1.10.88-dist.zip -d pdfjs && \
    mv /tmp/pdfjs/* /usr/share/javascript/pdf && \
    rm -rf /tmp/*

RUN useradd kyubey --create-home
USER kyubey

WORKDIR /tmp
ENV FLAG flag{fird_Party_Does_Fu3led_up__Du3lDu3lGo_3ant_even_hekp}
ENV G_SITEKEY 6Lfe2SEaAAAAAGurMvdKBjendG6oUDhdmOlVIvvj
ENV G_SECRET 6Lfe2SEaAAAAAJVLnkjcJ-A2qY0_CCVnGSiODCAo
ENV DISPLAY :99
CMD ["sh","-c","Xvfb :99 -screen 0 640x400x8 -nolisten tcp & python3 /server.py"] 