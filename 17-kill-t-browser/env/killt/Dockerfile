FROM python:buster
RUN apt-get -qqy update && \
    apt-get -qqy --no-install-recommends install \
    qutebrowser xvfb cron && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install flask

COPY server.py /
RUN echo '#!/bin/sh\necho b6actf{d1d_you_s0f_ahn_RCE_cha-l3n-gee_w1f-out_RCE}' > /proof_d2e4f0a6-55e8-4897-9ce0-e829cdc8279e.sh
RUN echo "#!/bin/sh\nrm -rf /tmp/*" > /cls
RUN chmod 555 /server.py /proof_*.sh /cls
RUN crontab -l | { cat; echo "*/30 * * * * /cls"; } | crontab

WORKDIR /usr/share/javascript/pdf
WORKDIR /tmp
# RUN wget https://github.com/ppcrab/CVE-2018-5158/raw/main/pdfjs-1.10.88-dist.zip
COPY pdfjs-1.10.88-dist.zip .
RUN unzip pdfjs-1.10.88-dist.zip -d pdfjs && \
    mv /tmp/pdfjs/* /usr/share/javascript/pdf && \
    rm -rf /tmp/*
RUN chmod -R 555 /usr/share/javascript/pdf

RUN useradd kyubey --create-home

WORKDIR /tmp
ENV G_SITEKEY 6Lfe2SEaAAAAAGurMvdKBjendG6oUDhdmOlVIvvj
ENV G_SECRET 6Lfe2SEaAAAAAJVLnkjcJ-A2qY0_CCVnGSiODCAo
ENV DISPLAY :99
CMD ["bash","-c","cron & Xvfb :99 -screen 0 640x400x8 -nolisten tcp & runuser -u kyubey -- python /server.py"]